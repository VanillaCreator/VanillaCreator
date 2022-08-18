# Crafts

1. Create crafts.yml
2. Write your receipes in yaml format

Here's a sample crafts.yml

``` yml
- name: sample_receipe1
  material:
    - id: minecraft:stone
      mod_id: sample:sampleitem1
      count: 24
    - id: minecraft:sugar
      mod_id: sample:sampleitem2
      count: 12
  product:
    - id: minecraft:grass_block
      mod_id: sample:sampleitem3
      count: 6
      name:
        text: A new item
        color: ffffff
      description:
        - text: Our past is everything we were
          color: 5bcfea
        - text: don't make us who we are
          color: eeeeee
    - id: minecraft:pink_dye
      mod_id: sample:sampleitem4
      count: 3
      description:
        - text: So I'll dream, until I make it real
          color: f5a9b8
        - text: and all I see is stars
          color: f5a9b8
  block:
    pos: on
    id: minecraft:crafting_table
- name: sample_receipe2
  material: minecraft:wheat
  product: minecraft:bread
```

name: an unique name for this receipe
product: can be a list or a single item
product.id: vanilla minecraft id of the item
product.mod_id
