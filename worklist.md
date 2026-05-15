# 📚 書庫數據建置工作清單

#### 📌 Phase 1：經典文學與哲學（來源：Standard Ebooks）— 最優先處理
*處理流程：直接去 Standard Ebooks 載 EPUB -> 丟進 Python 腳本拆成 JSON 資料夾。*
- [ ] **The Picture of Dorian Gray**（格雷的畫像）
- [ ] **The Great Gatsby**（大亨小傳）
- [ ] **1984**
- [ ] **The Adventures of Sherlock Holmes**（福爾摩斯探案集）
- [ ] **Frankenstein**（科學怪人）
- [ ] **Moby-Dick**（白鯨記）
- [ ] **The Book of Tea**（茶之書）
- [ ] **Bushido: The Soul of Japan**（武士道）
- [ ] **Brave New World**（美麗新世界）
- [ ] **Meditations**（沉思錄）
- [ ] **Beyond Good and Evil**（善惡的彼岸）
- [ ] **The Republic**（理想國）
- [ ] **The Prophet**（先知）
- [ ] **The Bible**（聖經 - 文學版）
- [ ] **The Count of Monte Cristo**（基督山恩仇記）
- [ ] **The Three Musketeers**（三劍客）

#### 📌 Phase 2：網路小說（來源：Royal Road / Novel Updates）— 需用工具抓取
*處理流程：用 `WebToEpub` 插件抓網頁 -> 轉成 EPUB -> 丟進 Python 腳本拆成 JSON。*
- [ ] **Mother of Learning**（Royal Road 天花板）
- [ ] **The Wandering Inn**（最長網文天花板）
- [ ] **無職轉生**（從 Novel Updates 找翻譯組連結）
- [ ] **關於我轉生變成史萊姆這檔事**（從 Novel Updates 找翻譯組連結）

#### 📌 Phase 3：其他名著與版權書（來源：圖書館 / 其他電子書站）— 需自行尋找乾淨 EPUB
- [ ] **Howl's Moving Castle**（哈爾移動城堡）
- [ ] **No Longer Human**（人間失格）
- [ ] **The Beast Player**（獸之奏者）
- [ ] **Dune**（沙丘）
- [ ] **The Hitchhiker's Guide to the Galaxy**（銀河便車指南）
- [ ] **The Catcher in the Rye**（麥田捕手）
- [ ] **The Protestant Ethic and the Spirit of Capitalism**（新教倫理與資本主義精神）
- [ ] **Orientalism**（東方主義）

#### 📌 Phase 4：系統整合與黑魔法
- [ ] **架設 TTS 串流後端**：用 FastAPI 寫好 `edge-tts` 的串流 API。
- [ ] **自動化批次處理**：寫一個 Python 迴圈，把下載下來的 EPUB 批次自動轉成 JSON 資料夾。
- [ ] **前端渲染測試**：將 Phase 1 產出的 JSON 餵給 `reader.html`，測試長文本滾動與播放流暢度。
