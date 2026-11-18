# 医保政策站点连通性测试（非营利）

本仓库仅用于验证 **GitHub Actions 的 ubuntu runner（海外环境）** 能否访问医保政策抓取源：国家医保局、云南省医保局、玉溪市政府门户及澄江市政府门户。

- 工作流：`.github/workflows/connectivity-probe.yml`
- 触发：推送到 main 自动触发，也可在 Actions 页手动 `Run workflow`。
- 探测内容：仅记录 HTTP 状态码、响应耗时、页面字节数与标题，不抓取正文、不写数据库、不含任何密钥。
- 结果判断：`可达 N/7`，200 即 runner 可访问该站点；超时/拒绝/证书错误等见备注列。
