# Locators

Do **not** commit UI dump XMLs here.

When you need a dump for locator discovery:

```bash
invoke ui:dump --screen=<screen_name>
```

That writes `docs/locators/<screen_name>.xml` locally. Use it to build/update page objects, then you may delete the XML afterward.

Page objects live in `src/page_objects/cofee/`. Flows: `docs/cofee-flow.md`.
