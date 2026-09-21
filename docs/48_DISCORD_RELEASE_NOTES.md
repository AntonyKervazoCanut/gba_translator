# Notes de version sur Discord

Le workflow `.github/workflows/release.yml` publie les notes dans
`#antony-releases` après la réussite de la publication GitHub (version immuable
et alias `latest`). Il lit le titre, les notes et le lien de `v2.1.<build>`
avec `gh release view` ; les notes sont donc celles de la release publiée.

Le secret GitHub Actions du dépôt `DISCORD_RELEASE_WEBHOOK_URL` contient l'URL
complète du webhook du salon. Ne jamais inscrire cette URL dans un fichier suivi
ou dans les logs. Pour remplacer le webhook, modifier ce secret dans les paramètres
Actions du dépôt. Aucun token de bot Discord n'est nécessaire.

Le message contient un titre cliquable et les notes. Les textes trop longs sont
tronqués avec `…` ; le lien conserve l'accès aux notes complètes et aux patchs.
Les mentions sont désactivées. Le transport utilise la confirmation `wait=true`
et un délai maximal de 30 secondes, sans afficher l'URL en cas d'erreur.

Un secret absent, un refus HTTP ou une erreur réseau fait échouer l'étape de
notification ; les releases déjà publiées restent disponibles. Il n'y a pas de
renvoi automatique : relancer le workflow renvoie une notification, même si cette
version a déjà été annoncée. Une expiration réseau peut survenir après livraison ;
vérifier le salon avant toute relance manuelle.

Vérification locale, sans publication ni appel à Discord :

```sh
python3 -m pytest tests/unit/test_notify_discord_release.py tests/unit/test_release_workflow.py -q
```

Le transport HTTP est simulé dans les tests. Aucun workflow distant n'est nécessaire
pour vérifier le contenu, les limites, les secrets ou la gestion des erreurs.
