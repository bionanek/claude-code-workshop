# Claude Code Workshop - slides

The presentation deck for the Claude Code workshop. 48 slides, browser-based.

## Presenting

Published at **https://bionanek.github.io/claude-code-workshop/** - the root URL opens the deck,
and `#20` on the end jumps straight to slide 20.

To present offline, download `slides.html` and open it in any browser. That one file is entirely
self-contained: the CSS, the JavaScript and every image are inlined, so it needs no server, no
internet connection and no other file in this repo.

Controls:

| Key | Action |
| --- | --- |
| `<-` / `->` | previous / next slide |
| `O` | overview grid, click a slide to jump |
| `B` | break screen (click it to type the return time), `B` or `Escape` to close |
| `F` | fullscreen |

## Editing

**Not here.** `slides.html` is generated output - editing it by hand works until the next rebuild
overwrites it. The generator, the host notes and the running script live in the separate workshop
project, and updated decks get copied into this repo.

This repo is the published deck and nothing else.

## What is in here

| File | Purpose |
| --- | --- |
| `slides.html` | the deck - the only file needed to present |
| `index.html` | one-line redirect so the GitHub Pages root URL opens the deck, preserving any `#n` slide hash |
| `.nojekyll` | tells GitHub Pages to serve the files as-is |
