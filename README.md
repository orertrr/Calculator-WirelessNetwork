# Next-Generation Wireless Network HW2

透過 TCP Socket 建立一個 Client-Server 架構的線上版計算機

## Progress

- [ ] 建立 TCP 連線環境
- [ ] Mode2 上傳檔案內容
- [ ] 將 Formula 拆分成 Tokens
  - [ ] Trim
  - [ ] 將 數字 及 運算子拆開
- [ ] 中序式轉後序式
- [ ] 計算
- [ ] 判斷錯誤

## Note

### Non-blocking socket

Server 的 socket 使用 accept 方法等待 client 連線，accept 會向作業系統呼叫 System call，此時程式將會停留在 accept()，直到有來自 client 的連線連入，因此這樣的形式被稱為 Blocking socket

但這樣有一個缺點，若使用者想要在此時中斷程式，通常是按 Ctrl+C 來向程式傳送 SIGINT 使程式中斷，但在 Python3.5 之後，accept 的機制變為當收到 SIGINT 信號時會重新呼叫 System call 而不是直接中斷，因此造成程式無法關閉

目前採用的方法為使用 Non-blocking socket，顧名思義就是當 accept 時不會等待連線連入，但當沒有連線連入時會產生錯誤，因此可以使用一個名為 select 的 System call