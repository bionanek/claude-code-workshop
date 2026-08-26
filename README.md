# Claude Code Workshop - slides

The presentation deck for the Claude Code workshop. 48 slides, browser-based, no build step
needed to present.

## Presenting

Published via GitHub Pages at **https://bionanek.github.io/claude-code-workshop/** - the root URL
opens the deck, and `#20` on the end jumps straight to slide 20.

Locally, open `slides.html` in any browser. That single file is fully self-contained - the CSS, the
JavaScript and both images are inlined, so it works offline and from a local file path.

Controls:

| Key | Action |
| --- | --- |
| `<-` / `->` | previous / next slide |
| `O` | overview grid, click a slide to jump |
| `B` | break screen (click it to type the return time), `B` or `Escape` to close |
| `F` | fullscreen |

You can also deep-link to a slide: `slides.html#20`.

## Editing

`slides.html` is **generated** - hand edits get overwritten. The source is `_build/gen_slides.py`,
where each slide is one `add(module_label, index_title, html)` call in presentation order.

To rebuild after editing:

```bash
python3 _build/gen_slides.py
```

That rewrites `slides.html` in the repo root. `index.html` is a permanent one-line redirect to it
for GitHub Pages and is not generated, so it never needs touching. Python 3 with no third-party packages is all it needs.

Notes on the source:

- The module label drives the on-screen header via the `HDR` map near the bottom of the file.
- The jump index (`O`) is built from the index titles automatically, so it cannot drift out of sync.
- `_build/assets/` holds the two images; they are base64-inlined into the output at build time.
- There are no break slides - the break screen is the `B` overlay, so it never shifts slide numbers.

## Checking a change

The deck auto-scales each slide to fit (floor 0.78), so content never clips - but anything scaling
below ~0.95 is rendering smaller than authored and should be trimmed instead. Open `slides.html`
at 1440x810 and run this in the browser console to list the offenders:

```js
[...document.querySelectorAll('.slide')].map((s,i)=>{
  s.classList.add('on'); const c=s.querySelector('.c'); c.style.transform='none';
  const cs=getComputedStyle(s);
  const avail=s.clientHeight-(parseFloat(cs.paddingTop)+parseFloat(cs.paddingBottom));
  const k=avail/c.scrollHeight; s.classList.remove('on');
  return k<0.95 ? [i+1,k.toFixed(2)] : null;
}).filter(Boolean)
```
