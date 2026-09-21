"""Notification de release : transport simulé, aucun message Discord réel."""

import json
from urllib.error import HTTPError, URLError

import pytest

from scripts import notify_discord_release as notify


@pytest.fixture
def release() -> dict:
    return {
        "name": "Unbound 2.1.43",
        "tagName": "v2.1.43",
        "body": '**Correctif français**\n"Écran" corrigé @everyone <@123>',
        "url": "https://github.com/example/project/releases/tag/v2.1.43",
    }


def test_posts_release_notes_and_link_without_mentions(monkeypatch, release) -> None:
    # Arrange
    requests = []

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

    def open_request(request, *, timeout):
        requests.append((request, timeout))
        return Response()

    monkeypatch.setattr(notify, "urlopen", open_request)

    # Act
    notify.publish("https://discord.com/api/webhooks/123/test-token", release)

    # Assert
    request, timeout = requests[0]
    payload = json.loads(request.data)
    assert request.method == "POST"
    assert request.full_url.endswith("?wait=true")
    assert timeout == 30
    assert payload["allowed_mentions"] == {"parse": []}
    assert payload["embeds"][0] == {
        "title": release["name"],
        "description": release["body"],
        "url": release["url"],
    }


def test_long_notes_keep_a_link_to_the_complete_release(release) -> None:
    # Arrange
    release["body"] = "É😀" * 5000
    release["name"] = "😀" * 300

    # Act
    embed = notify.build_payload(release)["embeds"][0]

    # Assert
    assert len(embed["description"].encode("utf-16-le")) // 2 <= 4096
    assert len(embed["title"].encode("utf-16-le")) // 2 <= 256
    assert embed["url"] == release["url"]
    assert embed["description"].endswith("…")


def test_empty_notes_and_title_have_fallbacks(release) -> None:
    # Arrange
    release.update(name="", body=None)

    # Act
    embed = notify.build_payload(release)["embeds"][0]

    # Assert
    assert embed["title"] == release["tagName"]
    assert embed["description"]


@pytest.mark.parametrize("webhook", ["", "http://discord.com/api/webhooks/1/token",
                                     "https://example.org/api/webhooks/1/token"])
def test_invalid_or_missing_secret_fails_before_network(webhook, release) -> None:
    # Act / Assert
    with pytest.raises(ValueError, match="DISCORD_RELEASE_WEBHOOK_URL"):
        notify.publish(webhook, release)


@pytest.mark.parametrize("error", [
    HTTPError("https://secret", 429, "secret-token", {}, None),
    URLError("secret-token"),
    TimeoutError("secret-token"),
], ids=["http", "network", "timeout"])
def test_transport_errors_never_disclose_the_secret(monkeypatch, release, error) -> None:
    # Arrange
    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(notify, "urlopen", fail)

    # Act / Assert
    with pytest.raises(RuntimeError) as caught:
        notify.publish("https://discord.com/api/webhooks/123/secret-token", release)
    assert "secret-token" not in str(caught.value)
    assert caught.value.__suppress_context__


def test_cli_reports_missing_secret_without_sending(tmp_path, monkeypatch, capsys, release) -> None:
    # Arrange
    source = tmp_path / "release.json"
    source.write_text(json.dumps(release), encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["notify_discord_release.py", str(source)])
    monkeypatch.delenv("DISCORD_RELEASE_WEBHOOK_URL", raising=False)

    # Act
    result = notify.main()

    # Assert
    assert result == 1
    assert "DISCORD_RELEASE_WEBHOOK_URL" in capsys.readouterr().err


def test_cli_reads_release_json_and_secret(tmp_path, monkeypatch, capsys, release) -> None:
    # Arrange
    source = tmp_path / "release.json"
    source.write_text(json.dumps(release), encoding="utf-8")
    calls = []
    monkeypatch.setattr("sys.argv", ["notify_discord_release.py", str(source)])
    monkeypatch.setenv("DISCORD_RELEASE_WEBHOOK_URL", "test-secret")
    monkeypatch.setattr(notify, "publish", lambda *args: calls.append(args))

    # Act
    result = notify.main()

    # Assert
    assert result == 0
    assert calls == [("test-secret", release)]
    assert "publiées" in capsys.readouterr().out
