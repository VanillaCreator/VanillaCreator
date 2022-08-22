craft_bases = {
    "detect": {
        "main": "execute as @e[type=minecraft:item,"
                "tag=!%%NS_LCF%%WillCraft%%RECEIPE_LCF%%,"
                "nbt={Item:%%ITEM%%}] at @s ",
        "others": "if entity @e[type=minecraft:item,distance=..1,"
                  "nbt={Item:%%ITEM%%}] ",
        "block": "if block %%POS%% %%ID%% ",
        "tag": "run tag @s add %%NS_LCF%%WillCraft%%RECEIPE_LCF%%\n"
    },
    "clear_others": "execute as @e[type=minecraft:item,tag=%%NS_LCF%%WillCraft%%RECEIPE_LCF%%] at @s "
                    "run kill @e[type=minecraft:item,distance=..1,limit=1,"
                    "nbt={Item:%%ITEM%%}]\n",
    "run_func": "execute as @e[type=minecraft:item,tag=%%NS_LCF%%WillCraft%%RECEIPE_LCF%%] at @s "
                "run function hrt:items/%%RECEIPE%%\n",
    "clear_self": "execute as @e[type=minecraft:item,tag=%%NS_LCF%%WillCraft%%RECEIPE_LCF%%] at @s "
                  "run kill @s\n",
    "gen_item": "summon minecraft:item ~ ~ ~ "
                "{Item:%%ITEM%%}"
}