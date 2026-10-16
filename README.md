# Kavel for Sublime Text

Kavel is a free AI video generator and AI image generator — 4K clips with sound, and images you can run without an account or a card. This package brings the image side into Sublime Text: select a line or type a prompt, keep writing, and the finished image's Markdown link lands where your cursor was.

## Use it

1. Open the Command Palette and run **Kavel: Generate Image**.
2. The prompt box is prefilled with your selection — edit it or press Enter.
3. About a minute later the image link is inserted below the cursor and its URL is on your clipboard:

```markdown
![a paper-cut fox in a moonlit forest](https://cdn.kavel.ai/uploads/…/….webp)
```

Generation runs in the background with a status-bar indicator, so the editor never freezes. No key is needed for a first try: calls run on Kavel's free allowance.

## Past the free allowance

Create an API key on your Kavel account at https://www.kavel.ai/settings/apikeys, then open **Preferences: Kavel Settings**:

```json
{
  "api_key": "sk-…",
  "model": "gpt-image-2"
}
```

With a key the call runs on your account: your credits, and the image models your [plan](https://www.kavel.ai/pricing?utm_source=sublime) includes.

| Setting | Default | What it does |
| --- | --- | --- |
| `api_key` | empty | Run on your Kavel account |
| `model` | free model | Model to use when a key is set |
| `aspect_ratio` | `1:1` | `16:9`, `9:16`, `4:3`, … |
| `insert_link` | `true` | `false` only copies the URL |

## More from Kavel

Editing a photo instead of starting from a prompt? Kavel keeps a page per edit — [hairstyle](https://www.kavel.ai/image/ai-hairstyle-changer?utm_source=sublime), [outfit](https://www.kavel.ai/image/ai-outfit-generator?utm_source=sublime) and the rest under [AI image tools](https://www.kavel.ai/image?utm_source=sublime). Video lives under [AI video tools](https://www.kavel.ai/video?utm_source=sublime).

Also for Vim and Neovim: [kavel.vim](https://github.com/hanshs474/kavel.vim).

MIT licensed.
