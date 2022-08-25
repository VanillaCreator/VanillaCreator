---
title: "Create Your First Project"
weight: 2
---

# Create Your First Project

{{<hint info>}}
A more user-friendly way to create project is still being developed, so create your project manually now :)
{{</hint>}}

## Create a project folder

Create a new folder under your workspace folder, name it to whatever you want (however recommend to same as the *project name* you set later)

## Create project config

Create a file named *project.yml* under your project folder and write these in yaml format

- name: Your project name (Only letters and numbers are allowed, and can`t be started with number)
- version: The version of your datapack, can be any string
- target: The minecraft version you want to deploy your datapack, can be a specific version or a range (Only 1.19 and 1.19.1 is supported now)
- description: Description of your datapack, multiline text is allowed, see [Text Format](../formats/text-format) for details

Here's an example:
``` yaml
name: hrt
version: v1.0
target: 1.19 - 1.19.1 # alt. 1.19.1 or 1.19
description:
  - text: HRT
    color: "#f5a9b8"
  - 今天你吃糖了吗?
```
