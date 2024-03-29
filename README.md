[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
<br>

<h1 align='center'> Parallel Web Server</h1>
<p align='center'>Web server that supports concurrent downloads and persistent connections</p>
<summary><h2 style="display: inline-block">Table of Contents</h2></summary>

- [About The Project](#about)
- [Siege Benchmark Results](#benchmark)
- [Requirements](#req)
- [Usage](#usage)
- [License](#license)
- [Acknowledgements](#ack)

<h2 id='about'>About The Project</h2>
<img src='Screenshot.png'>
<p>This parallel web server program supports concurrent HTTP requests from multiple web browsers using threads in Python. Simply put, if a website hosted a single 100GB file, and 1, 10, ... 200 clients tried to download the same file at the same time, their downloads should all make forward progress. The web server leaves the client connection open after serving a request. Additionally, the client has the option to send additional HTTP requests over the already-open socket. This reduces the latency of each request, because a new TCP connection does not have to be established. This program also supports graceful shutdown and verbose/silent mode.</p>

<h2 id='benchmark'>Siege Benchmark Results</h2>
<img src='Benchmark.png'>
<p> This program was benchmarked using Siege which is a multi-threaded http load testing and benchmarking utility. Siege was designed to let web developers measure the performance of their code under duress. The above table shows various performance statistics obtained from multiple 60 second tests as the number of concurrent clients increases from 1 (light workload) to 256 (heavy workload).</p>
<h2 id='req'>Requirements</h2>

* [Python 3](https://www.python.org)

<h2 id='usage'>Usage</h2>

```
Usage: server.py [-h] [--version] [--base BASE_DIR] [--port PORT] [--recv RECV] [--verbose]

Parallel Web Server

optional arguments:
  -h, --help       Show this help message and exit
  --version        Show Program's Version Number and Exit
  --base BASE_DIR  Base dir Containing Website
  --port PORT      Port Number to Listen On
  --recv RECV      Receive Size to Accommodate Incoming Data From the Network
  --verbose        Enable Debugging Output
```

<h2 id='license'>License</h2>
<p>Distributed under the MIT License.</p>

<h2 id='ack'>Acknowledgements</h2>

* [Siege](https://www.joedog.org/siege-home/)


[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/i0nics/parallel-web-server-python/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/bikramce
