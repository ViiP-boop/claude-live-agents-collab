# claude-agents-mesh

**Multi-agent, multi-machine communication for Claude Code — peer-to-peer, no extra server.**
**Communication multi-agents et multi-machines pour Claude Code — pair à pair, sans serveur ajouté.**

---

## 🇬🇧 English

### What this is

A simple pattern for letting **multiple Claude Code sessions talk to each other directly**, using two tools that are already shipped with Claude Code:

- `ListAgents` — list all Claude Code sessions reachable from this one (same account).
- `SendMessage` — push a message into another session's inbox.

No orchestrator. No file bus. No Redis. No LangGraph. Just sessions talking.

### 🔑 Across multiple machines

Thanks to **Remote Control**, every session connected to the *same Claude account* on *any PC, tablet or phone* becomes addressable from any other session. One account = one mesh across all your devices. A session on your PC can hand work to a specialist session running on your laptop, your tablet, or a server, in real time. **Machine-to-machine agent collaboration, for free.**

### Minimal example

Session **A** on PC (coordinator):
```
SendMessage(to="Android-specialist", message="Install APK on Fold 3 and return the sha of base.apk.")
```

Session **B** on a laptop (specialist) — receives it as a `cross-session-message`, runs its tool, replies:
```
SendMessage(to="agent-A", message="sha256 = c27397ef…befc5 — installed, 2 /sante OK.")
```

That's it. Each session is a Claude agent with its own identity, memory, tools, permission mode. They collaborate by **sending each other messages and acting on their own**, even across machines.

### Why this matters

Most multi-agent frameworks (LangGraph, AutoGen, CrewAI, OpenAI Swarm) assume a **single orchestrator** on a single machine that calls subagents and reads their results. Here it's **peer-to-peer AND multi-machine**: any session can message any other, on any device of the same account, with no boss.

Advantages observed in practice:
- **Real-time push** — the receiver is notified mid-turn, no polling.
- **Multi-machine for free** — Remote Control routes messages to sessions on different PCs/tablets of the same account.
- **Durable identity** — each session keeps its own history, so you can trust it to remember the mission.
- **Composable roles** — the "Android specialist" session stays the Android specialist across many parent tasks.

Limits — be honest:
- **Account-scoped.** Works only between Claude Code sessions on the **same account**.
- **Not a standard.** This is a Claude-specific transport, not a cross-vendor protocol.
- **No built-in backpressure, retries, or persistence.** The inbox is per-session.

### Reproduce

1. Open 2+ Claude Code sessions on your PC (give each a title / role). Optionally open more on another device logged in to the same account, with Remote Control on.
2. From one of them, call `ListAgents` — you should see the others (local + remote).
3. Call `SendMessage(to="<name of another session>", message="hello")`.
4. In the other session, the message arrives as `<cross-session-message from=…>` on its next turn.

That is the whole protocol.

### Patterns we use on top

- A **"thread" (le FIL)**: an HTTP service (any) where each session posts its current task, so newcomers can read what's going on without being spammed.
- A **"living room" (salon)**: same idea for free-form chat between sessions.
- A **"spider" (araignée)**: a tiny service that filters and routes who-needs-what to whom, so each session only sees what concerns it.

None of these are required. The two Claude Code tools are enough to start.

---

## 🇫🇷 Français

### De quoi il s'agit

Un schéma simple pour **faire discuter plusieurs sessions Claude Code entre elles**, en utilisant deux outils déjà fournis avec Claude Code :

- `ListAgents` — lister toutes les sessions Claude Code joignables (même compte).
- `SendMessage` — déposer un message dans la boîte d'une autre session.

Pas d'orchestrateur, pas de bus fichier, pas de Redis, pas de LangGraph. Juste des sessions qui se parlent.

### 🔑 À travers plusieurs machines

Grâce au **Remote Control**, toute session connectée au *même compte Claude* sur *n'importe quel PC, tablette ou téléphone* devient joignable depuis une autre session. Un compte = un maillage à travers tous tes appareils. Une session sur ton PC peut confier du travail à une session spécialiste sur ton portable, ta tablette ou un serveur, en temps réel. **Collaboration machine-à-machine entre agents, gratuite.**

### Exemple minimal

Session **A** sur PC (coordinatrice) :
```
SendMessage(to="spécialiste-Android", message="Installe l'APK sur le Fold 3 et rends le sha de base.apk.")
```

Session **B** sur un portable (spécialiste) — reçoit comme `cross-session-message`, lance son outil, répond :
```
SendMessage(to="agent-A", message="sha256 = c27397ef…befc5 — installé, 2 /sante OK.")
```

C'est tout. Chaque session est un agent Claude avec sa propre identité, mémoire, outils, mode de permission. Elles collaborent en **se donnant des messages et en agissant chacune de leur côté**, même sur des machines différentes.

### Pourquoi c'est intéressant

La plupart des frameworks multi-agents (LangGraph, AutoGen, CrewAI, OpenAI Swarm) supposent **un seul orchestrateur** sur une seule machine qui appelle des sous-agents et lit leurs résultats. Ici c'est **pair à pair ET multi-machines** : n'importe quelle session peut messager n'importe quelle autre, sur n'importe quel appareil du même compte, sans chef.

Avantages observés :
- **Push temps réel** — le destinataire est notifié en cours de tour, pas de polling.
- **Multi-machines gratuit** — Remote Control route les messages vers des sessions sur différents PC/tablettes du même compte.
- **Identité durable** — chaque session garde son historique, on peut lui confier une mission longue.
- **Rôles composables** — la session « spécialiste Android » reste spécialiste Android à travers plein de tâches parents.

Limites — soyons honnêtes :
- **Scopé au compte.** Marche seulement entre sessions Claude Code sur le **même compte**.
- **Pas un standard.** C'est un transport spécifique à Claude, pas un protocole inter-fournisseurs.
- **Pas de backpressure, pas de retry, pas de persistance intégrés.** L'inbox est par session.

### Reproduire

1. Ouvre au moins 2 sessions Claude Code sur ton PC (donne-leur un titre/rôle). Tu peux aussi en ouvrir sur un autre appareil connecté au même compte, avec Remote Control actif.
2. Depuis l'une, appelle `ListAgents` — tu dois voir les autres (locales + distantes).
3. Appelle `SendMessage(to="<nom d'une autre session>", message="hello")`.
4. Dans l'autre session, le message arrive comme `<cross-session-message from=…>` au tour suivant.

C'est tout le protocole.

### Patterns qu'on empile par-dessus

- Un **« fil »** : un petit service HTTP où chaque session poste sa tâche courante, pour que les arrivants lisent ce qui se passe sans spam.
- Un **« salon »** : pareil, mais pour la discussion libre entre sessions.
- Une **« araignée »** : minuscule service qui filtre et oriente qui-a-besoin-de-quoi, pour que chaque session ne voie que ce qui la concerne.

Aucun de ces trois n'est obligatoire. Les deux outils Claude Code suffisent pour démarrer.

---

## License / Licence

MIT — reproduce, adapt, publish. / MIT — reproduis, adapte, publie.

## Author / Auteur

[@ViiP-boop](https://github.com/ViiP-boop) — built and battle-tested inside the **OLYMPUS** home-system (6+ machines, Android tablets, Nintendo DSi, 30+ named Claude sessions across devices).

Construit et éprouvé dans le système maison **OLYMPUS** (6+ machines, tablettes Android, Nintendo DSi, 30+ sessions Claude nommées, réparties sur plusieurs appareils).
