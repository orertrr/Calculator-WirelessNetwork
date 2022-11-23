# Next-Generation Wireless Network HW2

透過 TCP Socket 建立一個 Client-Server 架構的線上版計算機

## Progress

- [x] 建立 TCP 連線環境
- [ ] Mode2 上傳檔案內容
- [x] 將 Formula 拆分成 Tokens
  - [x] Trim
  - [x] 將 數字 及 運算子拆開
- [ ] 中序式轉後序式
- [ ] 計算
- [ ] 判斷錯誤

## Test

```bash
$ python -m unittest test.test_calculator -v
```

## Note

### Blocking socket

Socket 有三種模式，分別為 Blocking、Non-Blocking、Timeout 三種，Socket 預設為 Blocking

Server 的 socket 使用 accept 方法等待 client 連線，accept 會向作業系統呼叫 System call，此時程式將會停留在 accept()，直到有來自 client 的連線連入，因此這樣的形式被稱為 Blocking socket

但這樣有一個缺點，若使用者想要在此時中斷程式，通常是按 Ctrl+C 來向程式傳送 SIGINT 使程式中斷，但在 Python3.5 之後，accept 的機制變為當收到 SIGINT 信號時會重新呼叫 System call 而不是直接中斷，因此造成程式無法關閉

目前採用的方式為另開一個 Thread 負責 socket 連線溝通，當 SocketThread 開始執行，Main Thread 便進入 sleep，當使用者愈中斷程式時，便會在 Main Thread 呼叫 server.close()，使 SocketThread 結束執行