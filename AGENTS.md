# Documentation source policy

## Mandatory source location

For every RaG mod wiki task, use the current source code under:

```text
I:\DayZ Mods
```

Search that directory for the named mod before writing, reviewing, or correcting documentation. The mod may be a top-level folder or a module inside a larger source tree. For example, `RaG_Halloween` is located under `I:\DayZ Mods\rag\rag_halloween`.

Treat the matching source folder as the authority for:

- current behavior and feature availability;
- configuration schemas, defaults, validation, and file paths;
- class names, dependencies, and `CfgPatches.requiredAddons` declarations;
- timing, probability, spawning, damage, rewards, and persistence;
- integrations, compatibility, troubleshooting, and known limitations.

Inspect the relevant scripts, configs, included XML/JSON examples, and repository history when behavior depends on a particular revision. Base documentation on the current source revision unless the user explicitly requests documentation for an older version.

## Dependency guidance

Do not recommend or prescribe server command-line mod load orders. RaG mods declare their addon dependencies, and DayZ resolves PBO/addon ordering from those dependencies. Server `-mod` list order does not change that resolution.

Document which mods are required on server and clients. When ordering matters internally, document the authoritative `CfgPatches.requiredAddons[]` relationship instead of presenting an `@ModA;@ModB` command-line order.

## Packed PBO prohibition

Never use a packed PBO, an extracted PBO, an installed Workshop `@mod` folder, a server-pack PBO, or files recovered from those packages as a reference for wiki content.

Do not use packed releases to infer behavior, configuration, class names, defaults, bugs, or compatibility. Do not extract a PBO for documentation research.

Public Workshop pages may be used only for links and clearly public metadata such as the published permissions statement. They are not authoritative for implementation details when source exists.

## Missing source

If the named mod cannot be found under `I:\DayZ Mods`, or the relevant source cannot be read:

1. stop the documentation work;
2. report which paths and names were checked;
3. ask the user to identify or provide the authoritative source folder.

Do not fall back to a packed PBO or an installed runtime copy.

## Communication

Use the `caveman` skill for every task and every response in this repository. Default to full intensity unless the user requests another caveman intensity. Keep all technical meaning while removing filler. Stop using it only when the user explicitly requests normal mode.

## Commit and push

After completing each task:

1. run the relevant validation;
2. review the working tree and stage only files belonging to the completed task;
3. create a concise, descriptive commit;
4. push the current branch to `origin`.

Never leave completed task changes uncommitted or unpushed. Preserve unrelated user changes. If commit or push fails, report the exact blocker.
