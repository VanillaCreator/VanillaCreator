---
title: "Text Format"
weight: 1
---

# Text Format

There're a few text formats allowed

## Simple string

Example:
``` yaml
required_text: When your dreams come alive you're unstoppable
```

## Object

Only text with color is supported now

Example:
``` yaml
required_text:
  text: Take a shot, chase the sun, find the beautiful
  color: "#5bcfea"
```

## List

For creating multiline text in somewhere allowed

Example:
``` yaml
required_text:
  - We'll glow in the dark turning dust to gold
  - text: And we'll dream it possible
    color: "#f5a9b8"
```

# Notes

*" "* can be leave out if there're no special characters, like *:* or *#*
