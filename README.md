[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
<br>

<h1 align='center'> Parallel Web Server Python </h1>
<p align='center'>Web server that supports concurrent downloads and persistent connections</p>
<summary><h2 style="display: inline-block">Table of Contents</h2></summary>

- [About The Project](#about)
- [Usage](#start)
- [License](#license)

<h2 id='about'>About The Project</h2>
<img src='Screenshot.png'>
<p>This parallel web servers upports concurrent requests from multiple web browsers using threads in Python. Simply put, if a website hosted a single 100GB file, and 1, 10, 100, ... 1000 clients tried to download the same file at the same time, their downloads should all make forward progress. The web server leaves the client connection open after serving a request. The client has the option to send additional HTTP requests over the already-open socket. This reduces the latency of each request, because a new TCP connection does not have to be established. This program also supports graceful shutdown and verbose/silent mode.</p>

<h2 id='start'>Usage</h2>

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

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/i0nics/parallel-web-server-python/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/bikramce
