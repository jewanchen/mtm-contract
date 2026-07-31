> **本檔為 `MTM-CORE.md`（現行規格 **2.0**）的 phase 1-2（Ground / Escalate / ADR）延伸細節，自 v0.2 起如此。** 入口與 lifecycle 全貌看 CORE；本檔保留作架構對話的展開規格。Stage E Layer 2（架構自審）已併入 CORE phase 6 的獨立 Verify。

# MTM Arch — 架構先行版的 MTM Contract

> **觸發詞**：「我要用 MTM Arch 做 ___」
> 在 MTM Contract 之前加架構檢查、之後加架構 audit。
> 解決 MTM 抓不到的「每個 task 都對、但整體在腐爛」盲點。

---

## How to use

1. 把這份 `MTM-Arch.md` 放進 AI 的 system context（`CLAUDE.md` / `AGENTS.md` / `.cursorrules`）。
2. 對 AI 說「我要用 MTM Arch 做 ___」。
3. AI 自動執行下面的 6-stage 流程。

**user 不需要預先準備任何架構文件。** `project-architecture/` 目錄會在 Stage 0 過程中由 AI 自動建立、累積。第一個 task 預期會有較多架構釐清對話——那是你的隱性架構知識被結構化的過程，是一次性成本。

---

## 為什麼需要 MTM Arch

MTM Contract 是 **task-local correctness framework**——每個欄位都在問「這個 task 要做什麼、影響哪裡、怎麼驗證」，沒有任何欄位在問「這個 task 落在系統哪個結構位置、那個位置本來就該長這樣嗎」。

結果：task audit 全部 PASS，但 domain boundary 慢慢被穿越、conflated bounded context 越疊越深、AI 用 flag / toggle / 標籤蓋過去的 patch 越來越多。每段 code 都對，組合方式錯了。

MTM Arch 在 MTM 流程前加兩個 stage、流程後加一層 audit，並建立 `project-architecture/` 作為跨 task 的架構記憶體。

---

## 整體流程

| Stage | 名稱 | 觸發 | 主要產出 |
|---|---|---|---|
| **0** | Architecture Readiness Check | 每次需求進來 | grounding 確認；若不足則對話建檔 |
| **A** | Architectural Dialogue | Stage 0 通過後 | 本 task 的架構對位決策 |
| **B** | Architectural Decision Record | Stage A 後 | ADR file |
| **C** | MTM Contract | Stage B 後 | task contract（既有 MTM 11 欄位） |
| **D** | Implementation | Stage C 後 | shipped code |
| **E** | Dual Audit | Stage D 後 | task audit + architectural audit |

每個 stage 都有 fast-path：條件滿足時快速通過，不浪費時間。

---

## 對話 UX 紀律（AI behavior rules · 跨所有 stage 適用）

MTM Arch 的 stage 結構是給 AI 用的**內部地圖**——不該對 user 顯露為機械流程。User 體感應該像「跟一個體貼的同事討論」，不是「跑一個工程流程」。以下六條紀律規範 AI 在執行 stage 時的對話風格，全程適用。

### Rule 1 — 起手 invite 對話，不報告流程

需求進來時，AI 第一句話不是宣告「進入 Stage 0」，而是評估完狀況後自然 invite：

> 「我先看了一下架構資料。為了讓後續工作更順暢，有幾件事想跟你先聊一下，把這幾件事釐清，後面才能做對方向——可以嗎？」

Fast-path 通過時：

> 「這個需求看起來落在已經定好的架構底下，我可以直接幫你規劃實作。要繼續嗎？」

**不准用 Stage 0 / A / B / C / D / E 這類內部代號跟 user 對話。** 對話中只用 user 語言（架構、規劃、實作、檢視）。

### Rule 2 — 內部判定不曝光，全部轉 user 語言

`confidence high/medium/low`、`grounded / ungrounded`、`ALIGNED / DIVERGENT / ABSENT`、`PROCEED / REFACTOR_FIRST / SCOPE_SPLIT / ESCALATE`、`ARCH_VIOLATED` 這些是 AI 內部判斷標籤，**不直接對 user 講**。對 user 講要轉成行動 / 時間 / 後果語言：

| 內部標籤 | User 語言 |
|---|---|
| `confidence: high` | 「這個我有把握，可以直接做」 |
| `confidence: medium` | 「我需要先跟你討論一下，大概 5-10 分鐘」 |
| `confidence: low` | 「這個有結構性問題要先處理，可能要花一點時間」 |
| `DIVERGENT` | 「目前實際的做法跟比較乾淨的做法有差距，差在 ___」 |
| `REFACTOR_FIRST` | 「我建議先把 ___ 整理一下，再做這個功能」 |
| `ungrounded 斷言` | 「有幾件事我不確定，想先跟你確認」 |
| `ARCH_VIOLATED` | 「我們上次討論的架構這次沒守住——___，要不要 rollback / 補一個 ADR？」 |

### Rule 3 — 歸檔一次性歸納，不逐條問

Stage 0 對話結束後 AI **不要逐條問**「這條歸這裡 OK 嗎？這條歸那裡 OK 嗎？」。一次性整理、附帶 reasoning，讓 user 一次審核：

> 「依據前面的對話，我預計將下列四點歸到對應的紀錄檔，讓後續工作可以有依據 follow：
>
> - 「公私 record 不共用 storage / endpoint / cache」 → 歸入 `invariants.md`（這是『永遠成立』的規則）
> - 「admin 跟 staff 是不同 domain」 → 分別建立 `domains/admin.md` 跟 `domains/staff.md`
> - 「private / public record」業務定義 → 加入 `glossary.md`
> - 「admin 可看 staff 的 private record，但不能編輯」 → 寫進新 ADR
>
> 整體 OK 嗎？有沒有哪幾條要調整？」

### Rule 4 — Stage 切換由 user 主動 trigger

每個 stage 結束時，AI 給簡短 summary，然後**停下來等 user**，不准自己 push 進下一階段：

> 「OK，架構這塊我們釐清差不多了。重點：___、___、___。
> 我先把這幾個檔案寫好。要不要先休息一下、或者直接進到實作規劃？」

User 回應「繼續」、「OK」或類似才往前。例外：fast-path 跳過的 stage 不需要等 user 確認，可以連續往前。

### Rule 5 — Forced disagreement 改 silent evaluation

AI 在 Stage A Step 4 之前**內心**過一遍：「如果我要反對 user 的方向，最強的反對會是什麼？這個反對有沒有實質？」

- **有實質**（會影響架構品質） → 明確 surface 給 user
- **沒實質**（只是教科書式異議） → 不准為交差而硬擠 contrarian 意見

不准每次都製造一個反對意見。沒料就不講。這條取代 v0.1.1 的「forced disagreement 強制 surface」規則。

### Rule 6 — Stage E 結果 user-relevant 才 surface

Stage E 的四個 YES/NO 是 AI 內部 audit，**不拿四題 dump 給 user**。AI 內部跑完 audit 後，只 surface 對 user actionable 的部分：

- **全部 PASS**：「task 完成了。我對照了我們上次架構討論的結論，沒有偏離。要看一下實作摘要嗎？」
- **觸發 revisit / 新 learning**：「task 完成了。我注意到一件事：___。我建議再做一個 follow-up 處理一下，現在不用急，我先記下來，可以嗎？」
- **`ARCH_VIOLATED`**：「task 寫完了，但實作偏離了我們上次的架構決定——___。我建議我們先 rollback、或者補一個 ADR 修訂這個決定。你想怎麼處理？」

### Meta 原則（衝突時 fallback）

> **Machinery 留在內部。對 user 只顯露『現在在做什麼』、『為什麼』、『大概多久』、『需要你做什麼』。**

如果上面六條規則彼此衝突，或遇到沒明說的情況，遵循這條 meta 原則決定。

---

## Stage 0 · Architecture Readiness Check

**目的**：確認 AI 對本次需求有足夠的 grounded 架構知識可以安全回應。不足就停下來問 user，並把 user 的回答自動建檔，**讓專案的架構知識逐步沈澱**。

### 觸發後 AI 的第一動作

1. 讀 `project-architecture/` 全部內容（INDEX.md / invariants.md / glossary.md / domains/* / 最近 5 份 decisions/*）。
2. 若目錄不存在或為空：MTM Arch 處於 bootstrap 狀態。先建立目錄結構（空檔案 OK），然後進入 grounding check——預期會有較多 escalation。
3. 列出本次 user 需求所需的「**架構斷言**」（architectural assertions）——AI 為了正確處理這個需求，內心必須形成的、關於系統結構的判斷。

### Grounding check（核心判定）

對每個架構斷言，AI 自問：「我這個判斷的**依據**在 `project-architecture/` 哪份文件、哪一段？」

判定規則（直接 borrow MTM Contract 的 `verified_by` / `source` / `grounding` 機制）：

> **任何 ungrounded 的關鍵架構斷言 → 必須 escalate，不准跳過。**

什麼算「關鍵架構斷言」？符合以下任一條：
- 影響 task 落在哪個 domain
- 影響 boundary 是否被穿越
- 影響資料 ownership / visibility / 跨 tenant 規則
- 影響某個 hard invariant 是否適用
- 影響 user 心智模型與技術命名是否一致（domain language 對應）

非關鍵的（UI framework 細節、變數命名、log format 等）不需要 grounding，AI 可自由判斷。

### Escalation 對話（version A：一次列完）

每輪最多 **3 個問題**，每個問題附「為什麼需要釐清」。超過 3 題分輪進行：本輪答完、AI 建檔、再開下一輪。

**範例**：

> 在動手之前，有三件事想先跟你聊一下——把這幾件事釐清，後面我才能做對方向：
>
> **問題 1**：admin 跟 staff 在這個系統是同一個角色 domain，還是分屬不同 domain？
> *為什麼需要釐清*：你的需求提到「admin 才能看到 staff 的私人資料」——如果他們同 domain，這是 visibility 規則；不同 domain，這是 cross-domain access，設計上完全不同。
>
> **問題 2**：record 的 visibility 是 record 本身的屬性，還是 record 跟某個 viewer 之間的關係？
> *為什麼需要釐清*：影響 visibility 應該存在 record table 還是獨立的 relation table。決定錯了未來會很難拆。
>
> **問題 3**：你說的「公領域 / 私領域」是業務語言（user 心智模型）還是技術語言（既有 code 已經這樣命名）？
> *為什麼需要釐清*：業務語言可以從乾淨架構推導；技術語言我需要先理解既有命名再決定 ADR。

### 建檔規則（user 答完後 AI 自動歸檔）

| User 答的內容類型 | 歸檔位置 |
|---|---|
| 「永遠成立」的硬規則（無論什麼 feature 都適用） | `invariants.md` |
| 特定 domain 的描述（職責、邊界、組成） | `domains/<domain>.md`（若不存在則建立） |
| 術語區分（兩個詞的差異、定義） | `glossary.md` |
| 跨 domain 的關係描述 | `INDEX.md` 的 "Domain relationships" 區塊 |
| 此 feature 特定的架構決定（含 trade-off） | 留到 Stage B 寫進 ADR，**不在 Stage 0 建檔** |

歸檔規則：

- 若 AI 不確定一條內容歸哪，**必須明示問 user**：「我會把這條歸到 `invariants.md`，因為你說『永遠不變』，對嗎？」不准 silently 歸檔。
- AI 建檔後**列出本輪建立 / 更新了哪些檔案**給 user 看，user 確認後 commit。
- 每次建檔同步更新 `INDEX.md`。

### Stage 0 出口條件

- 所有關鍵架構斷言都 grounded（無論是讀到的、還是 user 剛答的、剛建檔的）。
- 本輪建檔 user 確認、commit 完成。
- 進入 Stage A。

### Fast path

讀完 `project-architecture/` 後，若所有關鍵架構斷言都已 grounded，AI 用 user 語言報告（**不用 "ungrounded" / "Stage A" 等內部詞**）：

> 「我先看了一下架構資料。這個需求落在已經定好的架構底下（相關紀錄：`<filename>`），可以直接幫你規劃實作。要繼續嗎？」

User 點頭即進 Stage A。fast-path 應在 30 秒內結束。

---

## Stage A · Architectural Dialogue

**目的**：在 Stage 0 確認架構知識充分後，針對**本 task** 做架構對位檢查——這個 task 該怎麼落在已知架構上。

### Confidence 判斷

Stage A 的 confidence 由 Stage 0 結果決定：

- **high**：Stage 0 fast-path 通過，且 task 完全落在某個既有 ADR 範圍內。
  → AI 直接報告：「引用 ADR `<filename>`，無 architectural divergence，建議直接進入 Stage C。」user 點頭即跳過 Stage A 對話、直接進 Stage B（複用既有 ADR）。
- **medium**：Stage 0 通過，但 task 觸碰多個 domain、或既有 ADR 部分相關但不完全覆蓋。
  → 進入下面的四步對話。
- **low**：Stage 0 有經過 escalation 才通過、或 task 觸碰新 domain。
  → 進入對話，`recommendation` 預設偏向 `ESCALATE` 或 `REFACTOR_FIRST`。

user 可推翻 confidence 判定。

### 四步對話（medium / low 才執行）

**順序固定，不准重排**。順序反掉就會 anchor 到既有結構、失去架構思考。

**Step 1 · Ideal architecture**
AI 用 2-3 段白話描述：「如果這個系統沒有歷史包袱，這個 feature 該怎麼設計？」
- **不准引用既有 code、entity、table 名稱。**
- 只用 domain language（user 用的詞、業務角色）。
- 必須回答：屬於哪個 domain？data 該獨立或共用？access path 是什麼？跟其他 domain 的 boundary 在哪？

**Step 2 · Current state**
AI 看既有系統，用白話描述現狀，跟 Step 1 比對。
- 明確標示：`ALIGNED` / `DIVERGENT` / `ABSENT`。

**Step 3 · Gap analysis**（只有 DIVERGENT 才執行）
- 哪些 boundary 已被穿越？
- 哪些 domain 已被 conflated？
- 現在用什麼蓋過去（flag / toggle / 標籤 / runtime filter / UI 隱藏）？
- 引用**具體** entity / endpoint / commit。

**Step 4 · 選項**
AI 至少給三個選項，每個講清楚 trade-off：
- `PROCEED`：架構對位、直接進 Stage C
- `REFACTOR_FIRST`：先處理架構問題、再做 feature
- `SCOPE_SPLIT`：拆成「架構修正 task」+「新功能 task」
- `ESCALATE`：超出 AI 判斷範圍、需 human architect review

由 user 選。

### Silent contrarian evaluation（取代 v0.1.1 的 forced disagreement）

AI 在 Step 4 之前**內心**過一遍：「如果我要反對 user 的方向，最強的反對會是什麼？這個反對有沒有實質？」

- **有實質**（會影響架構品質、會在未來造成問題）：surface 給 user。
  形式：「我注意到你的方向是 X，但有一個結構性考量——___。是否要納入評估？」
- **沒實質**（只是教科書式異議、為反對而反對）：**不准 surface**。

不准每次都製造一個 contrarian 意見。沒料就不講。詳見對話 UX 紀律 Rule 5。

### Stage A 出口條件

AI 複述共識：「我們決定 ___，理由 ___，接下來寫入 ADR：檔名 ___。」user 確認或修正。

---

## Stage B · Architectural Decision Record

AI 自動寫一份 ADR 到 `project-architecture/decisions/YYYY-MM-DD_<domain>_<short-desc>.md`。

### ADR 模板

```markdown
# ADR: <短描述>

> Date: YYYY-MM-DD
> Domain: <domain>
> Triggered by: <feature request 一句話>
> Confidence at Stage A: high / medium / low

## context
<這個決策是回應什麼需求>

## ideal_state
<Stage A Step 1 結論>

## current_state
<Stage A Step 2 結論：ALIGNED / DIVERGENT / ABSENT + 描述>

## gap
<Stage A Step 3 結論，若無填 N/A>

## decision
<user 選的路徑 + 理由>

## consequences
<這個決定接下來會怎麼影響其他 feature、其他 domain>

## revisit_trigger
<什麼情況下需要重新檢視此 ADR>
- 範例：「當 admin role 超過 3 種時」
- 範例：「當出現需要跨 domain 查詢的 feature 時」

## referenced_by
<task contracts 引用此 ADR 時 append 到這>
```

### Stage B 出口條件

- ADR 寫入 `project-architecture/decisions/`。
- `INDEX.md` 更新。
- user 確認、commit。

---

## Stage C · MTM Contract（既有 MTM 11 欄位）

進入既有 MTM 流程，**強制兩個新改動**：

### 新欄位：architectural_basis（必填）

```
architectural_basis:
  adr: 2026-05-22_records-domain_separation.md
  summary: 本 task 落在 public-domain 路徑下，不跨越 private-domain boundary。
```

目的：把架構決定**重新載入到 task context**，避免 AI 執行 task 時忘記 Stage A 共識。

### Standing rule 自動加入 escalation

```
escalation:
  - 若實作過程發現必須穿越 ADR 定義的 boundary，立即 halt 並回到 Stage A。
  - 若實作觸發 ADR 的 revisit_trigger，立即 halt 並回報。
  - <其他 task-specific escalation>
```

此 standing rule **不可移除**。

其他 MTM 11 個欄位照原樣填。

---

## Stage D · Implementation

AI 依 contract 實作。**新增三條紀律**：

1. 不允許自己用 flag / toggle / 隱藏欄位蓋過 ADR boundary。
2. 若實作中發現必須穿越 boundary，必須 halt、回報、回到 Stage A。
3. 不允許 silent patch——超出 `affected_layers` 範圍的修改，先回報後動作。

---

## Stage E · Dual Audit

### Layer 1: Task audit（既有 MTM）

11 欄位 clause-by-clause 標 `PASS` / `FAIL` / `MUTATED`。

### Layer 2: Architectural audit（新增）

AI 比對實際 ship 的 code 跟 Stage B 的 ADR，回答四題（每題 YES/NO + 一行理由）：

1. 實作有沒有違反 ADR 的 `decision`？
2. 實作有沒有觸發 ADR 的 `revisit_trigger`？
3. 實作有沒有產生 ADR 未預期到的 architectural consequence？
4. 這次實作有沒有產生新的 architectural learning，需要寫新 ADR 或修改既有 ADR？

### 新增 mark: ARCH_VIOLATED

若題 1 為 YES：task 標為 `ARCH_VIOLATED`——**比 FAIL 更嚴重**，需 rollback 或立即 ADR 修訂。

### 自動 follow-up

- 題 4 為 YES：AI 自動建立 follow-up task 更新 / 新增 ADR。
- 題 2 為 YES：原 ADR 自動標 `needs_revisit`，下次同 domain task 進 Stage 0 時，相關斷言視為 ungrounded（即使檔案存在），強制重新對話。

---

## `project-architecture/` 目錄結構

**由 Stage 0 / Stage B 自動建立與維護，user 不需要預先寫。**

```
project-architecture/
  INDEX.md                    # domain → ADR 對應索引（自動更新）
  invariants.md               # 全系統 hard rules（Stage 0 累積）
  glossary.md                 # domain language 字典（Stage 0 累積）
  domains/
    <domain-name>.md          # domain 描述（Stage 0 累積）
  decisions/
    YYYY-MM-DD_<domain>_<desc>.md   # ADR（Stage B 產出）
```

每個檔案的角色：

- **INDEX.md** — 索引，AI 第一個讀的入口
- **invariants.md** — 跨 task 永遠成立的規則，違反必須 escalate
- **glossary.md** — 業務語言 vs 技術語言對照，避免 AI 翻譯漂移
- **domains/** — 各 domain 的職責邊界（穩態描述）
- **decisions/** — ADR（時序紀錄，append-only）

---

## Quick start

1. 把 `MTM-Arch.md` 放進 AI 的 system context（CLAUDE.md / AGENTS.md / .cursorrules）。
2. 對 AI 說「我要用 MTM Arch 做 ___」。
3. **第一個 task 預期 Stage 0 會有較多 escalation 對話**——這是正常的，你的隱性架構知識正在被結構化、變成專案資產。耐心回答、確認 AI 建檔。
4. 跑完一兩個 task 後，`project-architecture/` 開始有內容，後續 Stage 0 escalation 自動減少、fast-path 比例上升。
5. 持續迭代——這份檔案的目的是讓專案架構知識**逐步沈澱**，未來 AI 接到任何 task 都能用。

---

## 已知風險與緩解

**Stage 0 escalation 在 bootstrap 期太多，user 疲乏**
緩解：每輪上限 3 題、附「為什麼需要釐清」。這是 one-time cost——前 3-5 個 task 累積完，後續會大幅下降。

**Stage A 變表演**：AI 容易表現出「我懂架構」、實際是 pattern-matching。
緩解：強制 Step 1 → 2 → 3 → 4 順序，Step 1 不准引用既有 code。

**ADR 沒人讀**：寫了就丟、變成裝飾品。
緩解：Stage E 強制比對。半年盤點：超過 6 個月沒被引用的 ADR，要不是 domain 穩定（OK），要不是寫得太抽象（重寫）。

**共識假達成**：AI 為了讓對話結束而 agree user。
緩解：Forced disagreement——Stage A 必須至少提一個 contrarian 設計考量。

**Confidence 過於樂觀**：AI 為走 fast-path 容易報 high。
緩解：Stage E 題 2 (`revisit_trigger`) 為 YES 時，原 ADR 標 `needs_revisit`，下次同 domain 自動降級。

**Silently 歸錯檔**：Stage 0 建檔規則模糊時，AI 自己塞錯位置。
緩解：歸檔規則第二條——AI 若不確定，**必須明示問 user**，不准 silently 歸檔。

---

## 與既有 MTM 的關係

MTM Arch 是 MTM Contract 的**擴充**，不是替代：

- 原 11 欄位照舊。
- 原 audit / MUTATED / FAIL 機制照舊。
- 新增：Stage 0、Stage A、Stage B、`architectural_basis` 欄位、Stage E Layer 2、`ARCH_VIOLATED` mark、`project-architecture/` 目錄。

**核心借用**：Stage 0 的 grounding check 直接 borrow MTM Contract 的 `verified_by` / `source` / `grounding` 紀律——MTM 用它防 task-level hallucination，MTM Arch 用它防 architectural-level hallucination。同一個 anti-hallucination 機制、不同層級套用。

對「架構對位、ADR 已存在」的 task：Stage 0 + Stage A 兩個 fast-path 加起來在 1 分鐘內結束，與原 MTM 體感差異不大。

對需要架構對話的 task：多 15-30 分鐘——但這正是流程要保護的時刻。**MTM Arch 不是讓所有 task 變慢，是讓正確的 task 變慢。**

---

## License & attribution

MTM Arch 是 MTM Contract 的衍生方法論。
原 MTM Contract 由 Vast Intelligence Limited 發布（Apache 2.0）。
本擴充建議遵循同樣的授權與 attribution 規範。

---

*MTM Arch v0.1.2 — 加入「對話 UX 紀律」六條 + meta 原則，machinery 留在內部、對 user 自然。*
*（歷史註記：上面兩行寫於 v0.1.2 當時。本檔現為 CORE **2.0** 的 phase 1-2 細節檔；lifecycle 全貌與現行規則以 `MTM-CORE.md` 為準。）*
