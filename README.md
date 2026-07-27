# RaG Mod Wikis

Central Material for MkDocs site for the RaG DayZ mod documentation.

Published at <https://tyson89.github.io/RaG-Mod-Wikis/>.

## Preview locally

```powershell
python -m pip install -r requirements.txt
python -m mkdocs serve
```

Open the local address printed by MkDocs.

## Build the static site

```powershell
python -m mkdocs build --strict
```

The generated site is written to `site/`.

## Add another mod

1. Add the wiki repository and destination slug to `WIKIS` in `tools/import_wikis.py`.
2. Add the new mod to `nav` in `mkdocs.yml`.
3. Run `python tools/import_wikis.py`.
4. Review the imported links and run the strict build.

GitHub Wiki `_Sidebar.md` and `_Footer.md` files are deliberately excluded because navigation belongs in `mkdocs.yml`.

