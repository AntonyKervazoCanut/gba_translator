"""Mesure opt-in des fenêtres à colonnes et des tampons dynamiques du moteur."""
from __future__ import annotations


class EngineTextLayout:
    """Interprète uniquement les commandes qualifiées par le contrat de fenêtre.

    FC13 avance jusqu'à x_initial + argument sans jamais reculer. Un nom qui
    dépasse cette colonne décale donc silencieusement le prix dans le moteur :
    le contrat le refuse même si la largeur totale tiendrait dans la fenêtre.
    F7 est expansé avant impression, avec un index d'un octet et des réserves
    explicites en pixels et en octets (hors terminateur du tampon substitué).
    """

    @staticmethod
    def widths(raw: bytes, layout: dict) -> list[int]:
        """Retourne les largeurs et refuse les commandes ou expansions non bornées."""
        fonts = {int(key): bytes.fromhex(value['hex'])
                 for key, value in layout['engine_fonts'].items()}
        font = layout['initial_font']
        if font not in fonts or any(len(table) != 512 for table in fonts.values()):
            raise ValueError('Métriques moteur absentes ou incomplètes')
        widths = [0]
        expanded = 0
        i = 0
        while i < len(raw):
            value = raw[i]
            i += 1
            expanded += 1
            if value == 0xFF:
                if i != len(raw):
                    raise ValueError('Terminateur interne dans cette fenêtre')
                if expanded > layout['max_expanded_bytes']:
                    raise ValueError('Capacité du tampon expansé dépassée')
                return widths
            if value == 0xFE:
                widths.append(0)
            elif value == 0xFC:
                if i + 1 >= len(raw):
                    raise ValueError('Commande moteur tronquée')
                command, argument = raw[i:i + 2]
                i += 2
                expanded += 2
                if command == 0x06:
                    font = argument & 15
                    if font not in fonts:
                        raise ValueError('Police moteur non qualifiée')
                elif command == 0x13:
                    if widths[-1] > argument:
                        raise ValueError('Nom dépassant la colonne de prix')
                    widths[-1] = argument
                else:
                    raise ValueError('Commande moteur non qualifiée')
            elif value in (0xF7, 0xF8, 0xF9, 0xFD):
                if i >= len(raw):
                    raise ValueError('Commande moteur tronquée')
                argument = raw[i]
                i += 1
                expanded += 1
                if value == 0xF7:
                    buffer = layout.get('buffers', {}).get(str(argument))
                    if buffer is None:
                        raise ValueError('Tampon moteur non qualifié')
                    widths[-1] += buffer['max_width']
                    expanded += buffer['max_bytes'] - 2
                elif value == 0xF9:
                    widths[-1] += fonts[font][0x100 + argument]
                elif value == 0xF8 and argument < len(layout.get('keypad_widths', [])):
                    widths[-1] += layout['keypad_widths'][argument]
                else:
                    raise ValueError('Commande ou tampon moteur non qualifié')
            elif value in (0xFA, 0xFB):
                raise ValueError('Pagination interdite dans cette fenêtre')
            else:
                widths[-1] += fonts[font][value]
        raise ValueError('Terminateur absent dans cette fenêtre')
