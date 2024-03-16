# Demo of supported Markdown Features
This file serves as a reference for all supported markdown syntax.

# Basics
Markdown consists of simple syntax like `*cursive*` for *cursive*. You can also use `~~this~~` for ~~strikethrough~~ or `**bold**` for **bold**. A new paragraph starts by two newlines

Markdown is related to html and many html tags have markdown equivalents. Like headings or horizontal rulers. The equivalents to `h1` to `h6` are `#` to `######`.

---

This line above is a horizontal rule (hr) and you can create it with `---`


## Lists
1. You can do ordered or unordered lists
2. simply by starting a new line with `1.`
3. or `- ` for ordered/unordered respectively

- this is an unordered list
- simply for demonstration

There are a couple characters that start a list. `1.` and `1)` for ordered lists and `-`, `+` and `*` for unordered lists.

## Loose Lists
- list syntax also supports more complex ideas
    - like sublists. simply indent the list by atleast 4 spaces.
    
    [x] you can have paragraphs as part of a list element
- but as you can see that also changes the formatting of the list
- there now is a margin between each element all thanks to the line marked with [x]
- this is called a *loose* list and is a major point of confusion and even contention among developers working on markdown rendering

# Extended Syntax
To support more than the bare minimum of features we use several extensions.

## Table of Contents
You don't actually need to do anything for this. All headings automatically get referenced in a list of headings that floats at the side of the page.

## Tables
Tables are not markdown native but they're sometimes useful despite their awful syntax. Here's an example:

| column header | another header |
| :-----------: | :------------: |
|     item      |      item      |
|     item      |      item      |

This was achieved with the following code:

```
| column header | another header |
| :-----------: | :------------: |
|     item      |      item      |
|     item      |      item      |
```

## Fenced Code
What you just saw above is called *fenced code*. It allows you to wrap text into a specially styled block. It is technically preformatted text wrapped in a code tag. You can start it with a triple backtick, aka \`\`\`.

## Metadata
Sometimes you might want to include metadata into your markdown file. this usually gets stripped before being rendered. At the start of your file simply use the following syntax:
```
---
title: nice file title
tags: tutorial markdown
some other tag: some words
---
```

MarkWiki currently only makes use of the `tags` metadata though in the near future `title` may see some use.

## Word Definition
We use an extension that provides syntax for definition lists.

a word
: definition of `word`

Use the following syntax:

```
a word
: definition of `word`
: possibly another definition
```

## GitHub Checkbox Syntax
From github you might have been used to the following:

- [x] implement table of contents
- [x] implement edit history
- [/] improve lists
- [ ] add account management

This checkbox syntax is sometimes quite handy. You do it like so:

```
- [x] checked checkbox
- [/] indeterminate checkbox
- [ ] unchecked checkbox
```