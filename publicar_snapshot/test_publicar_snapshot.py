# -*- coding: utf-8 -*-
"""Testes do publicar_snapshot: rodam o script de verdade (bash + git) num repo de app descartavel,
com um repo "nu" local fazendo o papel do GitHub. Sem rede, sem importar nada de app.

Rodar da pasta que CONTEM publicar_snapshot/:
    python -m pytest publicar_snapshot -q
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent / "publicar_snapshot.sh"


def _bash() -> str | None:
    """No Windows, o bash do Git (o de System32 e o do WSL, que nao enxerga os caminhos)."""
    git = shutil.which("git")
    if git:
        for raiz in Path(git).resolve().parents:
            candidato = raiz / "bin" / "bash.exe"
            if candidato.is_file():
                return str(candidato)
    achado = shutil.which("bash")
    return None if (achado and "system32" in achado.lower()) else achado


BASH = _bash()
pytestmark = pytest.mark.skipif(BASH is None or shutil.which("git") is None, reason="precisa de bash e git")

ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
       "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_NOSYSTEM": "1"}

CONF = """REMOTO="github"
RAMO_PADRAO="main"
EXCLUIR=("_sessao/INTERNO.md")
TRAVA=('10[.]9[.]8[.]7' 'fulano[.]de[.]tal')
TRAVA_EXCETO=()
"""


def _git(pasta, *args) -> str:
    return subprocess.run(["git", *args], cwd=pasta, env=ENV, check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout.strip()


def _escrever(pasta: Path, arquivos: dict[str, str]) -> None:
    for caminho, texto in arquivos.items():
        alvo = pasta / caminho
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(texto, encoding="utf-8", newline="\n")


def _commit(app: Path, arquivos: dict[str, str], msg: str = "c") -> None:
    _escrever(app, arquivos)
    _git(app, "add", "-A")
    _git(app, "commit", "-q", "-m", msg)


def _rodar(app: Path, *args):
    return subprocess.run([BASH, "publicar_snapshot/publicar_snapshot.sh", *args], cwd=app, env=ENV,
                          capture_output=True, text=True, encoding="utf-8")


@pytest.fixture
def app(tmp_path):
    publico = tmp_path / "publico.git"
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(publico))
    app = tmp_path / "app"
    app.mkdir()
    _git(app, "init", "-q", "-b", "main")
    _git(app, "config", "core.autocrlf", "false")
    (app / "publicar_snapshot").mkdir()
    shutil.copy(SCRIPT, app / "publicar_snapshot" / "publicar_snapshot.sh")
    _commit(app, {"app.py": "print('oi')\n", "_sessao/INTERNO.md": "servidor 10.9.8.7\n",
                  "publicar_snapshot.conf": CONF}, "interno 1")
    _commit(app, {"app.py": "print('oi 2')\n"}, "interno 2")
    _git(app, "remote", "add", "github", str(publico))
    return app, publico


def _arquivos_publicos(publico: Path, ramo="main") -> set[str]:
    return set(_git(publico, "ls-tree", "-r", "--name-only", ramo).splitlines())


def test_versao():
    r = subprocess.run([BASH, str(SCRIPT), "--versao"], capture_output=True, text=True) if BASH else None
    assert r is not None and r.stdout.strip().startswith("publicar_snapshot ")


def test_primeiro_snapshot_sem_historico_interno_nem_arquivos_internos(app):
    app, publico = app
    r = _rodar(app)
    assert r.returncode == 0, r.stderr
    assert _arquivos_publicos(publico) == {"app.py", "publicar_snapshot/publicar_snapshot.sh"}
    assert _git(publico, "rev-list", "--count", "main") == "1"   # os 2 commits internos nao vao
    assert "Snapshot publico de main @" in _git(publico, "log", "-1", "--format=%s", "main")


def test_segundo_snapshot_descende_do_primeiro_e_repetir_nao_muda_nada(app):
    app, publico = app
    assert _rodar(app).returncode == 0
    _commit(app, {"app.py": "print('oi 3')\n"})
    assert _rodar(app).returncode == 0
    assert _git(publico, "rev-list", "--count", "main") == "2"
    r = _rodar(app)
    assert r.returncode == 0 and "ja esta atualizado" in r.stdout
    assert _git(publico, "rev-list", "--count", "main") == "2"


def test_trava_aborta_com_dado_interno_e_nada_sai(app):
    app, publico = app
    _commit(app, {"config.py": "HOST = '10.9.8.7'\n"})
    r = _rodar(app)
    assert r.returncode == 1 and "ABORTADO" in r.stderr and "config.py" in r.stdout
    assert _git(publico, "branch", "--list") == ""   # nada foi enviado


def test_trava_ignora_caminho_em_TRAVA_EXCETO(app):
    app, publico = app
    _commit(app, {"docs/nota.md": "fulano.de.tal\n",
                  "publicar_snapshot.conf": CONF.replace("TRAVA_EXCETO=()", 'TRAVA_EXCETO=("docs/")')})
    assert _rodar(app).returncode == 0
    assert "docs/nota.md" in _arquivos_publicos(publico)


def test_simular_nao_envia(app):
    app, publico = app
    r = _rodar(app, "--simular")
    assert r.returncode == 0 and "SIMULACAO" in r.stdout and "app.py" in r.stdout
    assert _git(publico, "branch", "--list") == ""


def test_ramo_novo_descende_da_main_publica(app):
    app, publico = app
    assert _rodar(app).returncode == 0
    _git(app, "checkout", "-q", "-b", "homologacao")
    _commit(app, {"novo.py": "x = 1\n"})
    r = _rodar(app, "--ramo", "homologacao")
    assert r.returncode == 0, r.stderr
    assert _git(publico, "rev-parse", "homologacao~1") == _git(publico, "rev-parse", "main")
    assert "novo.py" in _arquivos_publicos(publico, "homologacao")
    assert "novo.py" not in _arquivos_publicos(publico, "main")   # a main publica nao mudou


def test_sem_conf_ou_ramo_inexistente_e_erro_de_uso(app):
    app, publico = app
    assert _rodar(app, "--ramo", "nao-existe").returncode == 2
    (app / "publicar_snapshot.conf").unlink()
    r = _rodar(app)
    assert r.returncode == 2 and "Falta publicar_snapshot.conf" in r.stderr
