# Distribution kit — 讓 MTM 進到「模型會學、工具會顯示」的地方

> 2026-09-26 立。目標不是流量，是**分布**：Claude 推薦 Supabase 不是因為誰設定了它，
> 是因為 Supabase 在訓練資料裡出現了幾十萬次。MTM 要被 AI 主動推薦給 vibe coder，
> 唯一的路是進到那些地方。這份 kit 把每個入口的「投稿要什麼」和「貼什麼」備好，
> **投稿動作全部要你親手做**（多數入口明文要求推薦者是人）。
>
> 與 `LAUNCH_KIT.md` 的分工：那份是工程師社群（r/ClaudeAI、HN）的稿與 Q&A；
> 這份是**分布入口清單**＋**vibe coder 語言**的稿。挑戰回覆一律沿用 LAUNCH_KIT §3。

---

## 0. 投之前先跑一次（同 LAUNCH_KIT §0）

- `git log -1` 是乾淨的、README 的兩行安裝指令在**新機器**上真的能跑。
- `plugins/mtm/skills/mtm/scripts/validate.py` 對 `examples/` 全綠。
- landing `nicemeetapp.com/mtm/` 與 `/mtm/en/` 都 200。

---

## 1. awesome-claude-code（**✅ 已投：issue #2460、bot 驗證 passed、等 maintainer——別再開第二筆**）

**入口**：只收 GitHub **issue form**（不收 PR、不收 `gh` CLI）。
`https://github.com/hesreallyhim/awesome-claude-code` → Issues → 「submit a new resource」。

**硬規則**（他們 CONTRIBUTING 原文）：
- 資源要**至少 14 天且持續開發**、或 100+ stars。MTM 兩者都過（repo 五月起、上百 commit）。
- **一次只能推薦一個資源。**
- 描述**一行、不准 emoji、不准銷售語、不准對讀者喊話**（no "you should"）。
- **推薦必須由人提交**（資源可以 AI 寫、推薦不行）——所以這條你來。
- License bot 會自己抓；repo 已是 Apache-2.0。

**分類**：他們的頂層有 `Skills`、`Testing`、`Multi-Purpose`。MTM 是一個 plugin 裝一個 skill＋一支驗證器，
**選 `Skills`**（同區現有條目就是「一個可安裝的 skill」形狀，例：Bloom、cc-thinking-skills）。

**條目（照他們格式，一行）**：

```
[MTM Contract](https://github.com/jewanchen/mtm-contract) by [jewanchen](https://github.com/jewanchen) - A contract-first skill that has the agent classify a task by observable triggers, write down what must already be true and how it was checked before generating code, refuse to mark a check passed on a promise, and pull in a clean-context reviewer before risky merges; ships a standard-library-only validator that fails the contract file when a "verified" claim has no recorded observation.
```

（上面那行 96 字以內的英文摘要如果表單有字數上限，砍成：）

```
A contract-first Claude Code skill: the agent writes down what must be true and how it checked, before it generates code; a bundled validator fails any "verified" claim that has no recorded observation.
```

**表單欄位對照**：Name＝`MTM Contract`；Link＝repo；Category＝Skills；Description＝上面那行；
License＝Apache-2.0（bot 會抓）。

---

## 2. 官方 plugin 目錄（`/plugin` 搜得到的那個）

> 投稿方式見本檔 §2.1（2026-09-26 查證結果補上）。

### 2.1 查證結果（2026-09-26，來源 claude.com/docs/plugins/submit、/plugins/pre-submission-checklist、/directory/publish）

- **入口**：developer portal `https://claude.ai/directory/manage` → **Submit new** → **Plugin bundle** → 填 repo
  `jewanchen/mtm-contract`＋**Plugin path `plugins/mtm`**（plugin 不在 repo 根目錄就要填）→ **Validate**。
- **資格**：claude.ai **Pro／Max／Team／Enterprise**（Free 不行）；Pro/Max 直接用自己帳號；
  **GitHub 帳號要先在 claude.ai 連結、且對 repo 有 push 權**（portal 會查）。
- **上線後**：merge 到 main 就自動抓新版、掃描、（依設定）自動發布；`version` 每次發版要升。
  一個組織一天最多 10 次提交；同一 repo+資料夾只能一個組織擁有。
- **審核**：自動驗證＋安全掃描＋**第一版一定有真人看**；review 時間不固定。
- **會擋的（Blocks）我已處理**：①`LICENSE` 必須在 **plugin 資料夾內**或 `plugin.json` 寫 `license`——
  原本只有 repo 根目錄一份 → 已複製到 `plugins/mtm/LICENSE` 並加 `"license": "Apache-2.0"`
  ②README ≥40 字（有，853 字）③`.DS_Store` 等系統檔（無）④非圖片檔 <256 KiB、≤512 檔（過）。
- **會被 hold 給真人看的**：名稱像既有品牌／全是通用字。`mtm` 三個字母、`displayName` 已設
  `MTM Contract`、`author.name` 是公司名——都不是通用字，但 **hold 不是拒絕**，第一版本來就會有人看。
- **安全掃描看什麼**：未揭露的對外傳送／隱藏程式碼／改權限。MTM 只有一支標準庫 Python
  驗證器（SKILL.md 叫 Claude 跑、不是 hook）、零網路呼叫——README 已寫明。
- **本機預檢**：`claude plugin validate ./plugins/mtm` → ✔ Validation passed（2026-09-26）。
- **表單的 Data handling 四題怎麼答**：不讀不存個資（契約檔寫在使用者自己的 repo）／
  不送資料到任何服務／不保留資料／非針對 18 歲以下。

### 2.2 目錄要的 metadata（現況檢查）

| 欄位 | 現值 | 要動嗎 |
|---|---|---|
| `plugin.json.name` | `mtm` | 不動（安裝指令已印在文件與 landing） |
| `plugin.json.version` | `2.5.0` | 不動；**改規則才升版**（你定的 gate） |
| `plugin.json.description` | "Contract-first discipline for delegating implementation to an agent, with a bundled zero-dependency validator." | 不動（目錄列表的描述讀 README，不讀這欄） |
| `plugin.json.license`／`displayName`／`repository`／`keywords` | **09-26 新增**（license 是 Blocks 項） | 已補、不升版 |
| `marketplace.json.category` | `development` | 目錄沒有分類欄、照 README 內容自動歸類；不動 |
| README | `plugins/mtm/README.md` 有安裝／更新／版本查法 | 夠 |
| LICENSE | Apache-2.0 | 夠 |

---

## 3. 給 vibe coder 的稿（語言換掉，內容不變）

工程師社群的稿講 hallucination 和 verification。Vibe coder 不講這些詞，他們講的是
**「它說修好了，我按下去，沒好」**和**「同一個 bug 它修第三次了」**。稿只換這件事。

### 3.1 r/vibecoding（英文）

**標題**

```
The rule that stopped my AI from saying "fixed" when it wasn't
```

**內文**

```
I don't read most of the code my agent writes. Which means the only thing I
have is what it tells me — and "done, verified" costs it nothing to type.

So I gave it a rule set (MTM). Short version:

- Before it builds anything non-trivial, it writes three lines: what will be
  true when this works, what it's NOT allowed to decide alone, and what it's
  touching / not touching. If my request could mean two different things in
  the data, it lists both and asks instead of picking one.
- It cannot mark anything "verified" unless it shows what it actually ran —
  the command, the query, the log line. "Will check later" fails a little
  script that comes with it.
- If a fix doesn't work the first time, it is not allowed to try another
  fix. It has to stop and establish one fact first. This one alone ended the
  "fixed it → broke something else → fixed that → first bug is back" loop
  for me.
- Anything risky (auth, payments, database changes) gets reviewed by a
  second agent that never saw the code being written.

Typos, styling, one-file changes skip all of it. It's built to be skipped.

Nothing to install if you don't want to: paste one file to your AI and say
"set this up". It asks you one question and you're done. Claude Code users
can install it as a plugin in two commands.

No benchmark, one codebase (mine), Apache-2.0. If it does nothing for you
there's an issue template that asks exactly that.

github.com/jewanchen/mtm-contract
```

### 3.2 Threads／FB 社團（中文）

**版本 A（短、給 Threads）**

```
我不看 AI 寫的 code。所以它說「修好了」我只能信。

後來給它一套規則（MTM），最有感的三條：
① 修 bug 第一次沒好，不准再猜第二次，先停下來查一個事實。
② 說「驗證過了」要貼出它跑了什麼，沒貼就不算。
③ 我的需求如果在資料上可能指兩件事，它要列出來問我，不准挑一個猜。

貼一份檔案給你的 AI、說「幫我設定」就好，不用裝東西。
Claude Code 兩行指令可裝 plugin。開源、免費。

github.com/jewanchen/mtm-contract
```

**版本 B（長、給 FB 社團或 blog）**

```
用 AI 寫東西的人大概都經歷過這個循環：它說修好了，你一按，沒好；它再修，
另一個地方壞了；它再修，第一個 bug 回來了。你不看 code，所以只能一直信它。

問題不在它不會寫，在它「說驗證過了」跟「真的驗證過」對它來說成本一樣低。

MTM 是一套給 AI 的工作規則，只做一件事：把便宜的查證擺到昂貴的生成之前。
具體是四條：

1. 開工前先寫三行：做完會看到什麼、哪些事它不能自己決定、它會動到哪裡。
   你的話如果在資料裡可能指兩種東西，它要列出來問，不准挑一個就做。
2. 「驗證過了」要附證據：它跑了哪個指令、查了哪筆資料、看到什麼。
   沒有的話一支小腳本會把那份文件判失敗。
3. 修 bug 第一次沒好，不准再修。先停下來確認一個事實。
4. 碰到登入、金流、資料庫這種事，要另一個沒看過過程的 AI 來看一遍再合併。

改個錯字、調個顏色、動一個檔案的小事全部跳過，它就是設計來被跳過的。

用法最簡單是把 repo 裡那份「交給你的 AI」檔貼給它、說「幫我設定」，它會問你
一個問題然後就好了。Claude Code 的話兩行指令裝 plugin。

沒有 benchmark、只在我自己一個專案上用了幾個月，開源 Apache-2.0。
覺得沒用的話 repo 有個 issue 範本就是問這個。

github.com/jewanchen/mtm-contract
```

### 3.3 這個族群會問的三題（LAUNCH_KIT §3 沒有的）

**「我不會看契約，寫了給誰看？」**
給下一輪的 AI 看。你不用讀，但它第二次修同一個 bug 時會先看到自己上次猜了什麼。
最短的版本三行，多數任務連三行都不寫。

**「這不就是叫它『小心一點』？」**
「小心一點」沒有失敗條件。MTM 有：說驗證過但沒貼跑了什麼＝失敗，第一次修不好還再猜＝違規。
有失敗條件的規則才會被遵守。

**「token 會不會變多？」**
會，寫契約那幾行是多的。省下來的是修錯方向那幾輪。沒有數字，不編。

---

## 4. Landing 頁讓 vibe coder 搜得到（**✅ 09-26 已改 meta description、nicemeet `93ee6c4`；FAQ 段未加**）

現在的 title／description 是工程師語言（「把便宜的查證擺到昂貴的生成之前」），
搜「AI 一直說修好了」「vibe coding 一直改壞」找不到。**建議只改 `<meta description>` 和加一段 FAQ，
`<title>` 與 h1 不動**（品牌句留著）。

- zh description 提案：
  `AI 說修好了但沒好？MTM 是給 AI 的一套工作規則：開工前先寫下要查什麼、說「驗證過」要附證據、修不好不准再猜。貼一份檔案給你的 AI 就能用；Claude Code 兩行指令裝 plugin。開源免費。`
- en description 提案：
  `Your AI says "fixed" and it isn't? MTM is a rule set for coding agents: write down what to check before building, show what was actually run before claiming "verified", and stop guessing after a failed fix. Paste one file to your AI, or install as a Claude Code plugin. Free, Apache-2.0.`
- 加一段 `<h2>` FAQ（三題＝§3.3），用問句當標題，那就是搜尋字串。

---

## 5. plugin 觸發描述（**✅ 09-26 已加、`381b85a`、未升版**）

現在 `SKILL.md` 的 description 只有工程師的觸發詞（schema change、tenant visibility、auth）。
Vibe coder 不會講這些，skill 就不會在他們需要時被載入。**§7「從零開始」早就寫好了，只是描述沒讓它出現。**

建議在 description 尾端加一句（其餘不動）：

```
Also use when the user asks for a whole product or feature from one sentence, when the same bug is being fixed a second time, when the user says they do not read the code and are relying on the agent's own word, or when a request would silently pick one interpretation of ambiguous data.
```

這不是規則改動（§1-§9 一字未改），是**觸發面**改動，所以我建議不升 2.5.x。
但它會改變 skill 何時自動啟動，等你點頭。

---

## 6. 順序建議

1. §1 awesome-claude-code（你填表單，五分鐘；14 天規則早就過）。
2. §3.2 版本 A 貼 Threads、版本 B 貼一個 FB 社團；§3.1 貼 r/vibecoding。**前三小時待在串上**（LAUNCH_KIT §4）。
3. §2 官方目錄（依 §2.1 查證結果）。
4. ~~§4、§5~~ 已做（09-26）。
5. 貼完隔天照 LAUNCH_KIT §5：真的被問的問題補進 §3.3。
