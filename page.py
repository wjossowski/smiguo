def render_page():
  site = """
    <html>
      <head>
        <script src="//unpkg.com/alpinejs" defer></script>
      </head>
      <body>
        <h1>Siemanko</h1>
        <h2>Witaj w komnacie tajemnic</h2>
        <div x-data="boardData()" x-init="init()">
          <pre x-text="text"></pre>
          <p>
            <button @click="await setAngle(angle - 180)">-180</button>
            <button @click="await setAngle(angle - 90)">-90</button>
            <button @click="await setAngle(angle - 60)">-60</button>
            <button @click="await setAngle(angle - 30)">-30</button>
            <button @click="await setAngle(angle - 15)">-15</button>
          </p>
          <p>
            <button @click="await setAngle(90)">RESET (90)</button>
          </p>
          <p>
            <button @click="await setAngle(angle + 15)">+15</button>
            <button @click="await setAngle(angle + 30)">+30</button>
            <button @click="await setAngle(angle + 60)">+60</button>
            <button @click="await setAngle(angle + 90)">+90</button>
            <button @click="await setAngle(angle + 180)">+180</button>
          </p>
        </div>
        <script>
          function boardData() {
            return {
              angle: 90,
              text: "loading...",
              setAngle(a) { fetch('/motor?a=' + a, { method: "POST" }) },
              getData() { fetch('/data').then(r => r.json()).then(data => {
                  console.log(data)
                  this.angle = data.angle
                  this.text = data.text
                })
              },
              init() { setInterval(() => this.getData(), 4000) }
            }
          }
        </script>
      </body>
    </html>
    """
  return site
