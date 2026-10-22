[中文](README.md) · English

# oil-ui-pro

An interface design method for AI agents. It explores a few genuinely different directions side by side, lets you choose one, then refines it against real screenshots. It works for websites, apps, dashboards, and components, and it can also just review a design.

See more designs at [ui.oiloil.org](https://ui.oiloil.org).

## Installation

Send this to your agent:

```text
Install Oil UI Pro for me: run npx github:oil-oil/oil-cli install oil-ui-pro
```

You can also run the command in your terminal yourself. The first install opens a browser: sign in with the oiloil account you used to purchase it and click “Allow.”

It's ready to use right after installation, with nothing to configure. When a new version is out, your agent mentions it at the end of a reply; ask it to update whenever you like. With Oil UI Pro installed, you don't need the open-source Oil UI. Installing both makes them compete for the same requests.

## Usage

Tell your agent what you need, for example:

- “Use oil-ui-pro to explore a few design directions for this course booking product and build pages I can preview.”
- “Create three designs with different typography, colors, and compositions. Put them on a comparison page so I can choose.”
- “Keep the current brand and layout. Improve this form’s hierarchy, error messages, and mobile experience.”
- “Polish this page using the project’s existing design guidelines.”
- “Review these interfaces and explain what to change and how. Leave the files untouched.”

Share any brand assets, screenshots, or existing project you have. It can start without references and only asks you questions when the deliverable is unclear.

## How it works

- **Explore distinct directions, then let you choose.** It first works out what the product is and how the best products in its category handle it, then derives a tone from the product itself and develops a few concrete directions. Each direction settles its first-screen layout before any copy is written, and it checks that the directions really differ. The previews go on one comparison page; you choose one and say what you like and dislike.
- **Leave one moment people remember.** Instead of pushing every part of the page, it makes one or two details exceptional, such as the response to a tap, a successful payment, AI at work, or a 404 page. Everything else stays quiet.
- **Refine against real screenshots.** It checks the result at desktop and mobile sizes, then brings in a reviewer who hasn't seen the work in progress to find problems and give a score. It revises and reviews again, aiming for 9/10 within three rounds. With several directions, a side-by-side review catches sections that look alike; for new interfaces, the reviewer actually completes real tasks on the page.
- **Make interfaces easy to use.** Interactions and states, forms, dialogs and popovers, and desktop and mobile layouts each come with concrete practices. For dashboards and tools, it picks a workspace layout that fits what the product handles, and carries the style from the first screen all the way down.
- **Polish a single component to the extreme.** It starts with a visual anchor, such as a realistic product render, takes the palette from it, and picks one graphic motif to carry throughout. From two or three sketches it develops just one: every state gets its own visual, and the main interaction acts directly on the anchor, so results appear as you drag. Review rounds check it up close, and it finishes with a showcase image and a short screen recording.
- **Start an existing project by working out what you want.** If it looks dated, it first decides whether the current design system is worth keeping, then offers options from a light cleanup to a full reshape. If it's hard to use, it walks through the real task itself, finds out why the extra steps exist, and fixes the structure instead of adding a hint. For a new feature, it learns the product's existing habits first, then proposes genuinely different ways to do the job while keeping the current visual system. Changes go into shared components and design tokens; something as small as a single button gets changed directly.

There are methods for visual hierarchy, typography, color, spacing, imagery, motion, scroll storytelling, and effects such as light trails, dot patterns, and flowing gradients. It won't push every product into the same style, and it won't add generated images, animation, or effects to every page. It uses them only where they help.

## Built-in style comparison page

When you want to compare designs, it puts them side by side on one page. They can be HTML files, images, or running development pages, and the current version can go first as a baseline. You can switch between desktop and mobile sizes, open each one at actual size, and browse with the arrow keys. Click “Select” on the one you like, paste the copied sentence into your agent, and it carries on from there.

## Version checks

Each time it is used, the Skill checks for a newer version, going online at most once every 10 minutes. It only reads the public version list at ui.oiloil.org and uploads nothing from your project. By default it only tells you about an update; it downloads and replaces nothing unless you explicitly ask it to update. Results are cached in `~/.local/state/oil/` (or `XDG_STATE_HOME` when set; `%LOCALAPPDATA%\oil\` on Windows). It needs Python 3. Set `OIL_NO_UPDATE_CHECK=1` to turn it off.

## Use with

- [oil-motion](https://github.com/oil-oil/oil-motion): Turn generated videos or frame sequences into web animation controlled by scrolling or dragging, such as product teardowns or camera fly-throughs. Use it for a striking opening animation.
- [oil-tone](https://github.com/oil-oil/oil-tone): Rewrites headings, descriptions and intro copy so they read naturally and clearly, in Chinese or English. Use it when the copy feels machine-written or awkward.
