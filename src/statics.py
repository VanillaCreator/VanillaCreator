craft_bases = {
    "detect": {
        "main": "execute as @e[type=minecraft:item,"
                "tag=!%%PROJECT_NAME_LCF%%WillCraft%%CRAFT_NAME_UCF%%,"
                "nbt={Item:{id:\"%%ID%%\",Count:%%COUNT%%b}}] at @s ",
        "others": "if entity @e[type=minecraft:item,distance=..1,"
                  "nbt={Item:{id:\"%%ID%%\",Count:%%COUNT%%b}}] ",
        "block": "if block %%BLOCK_POS%% %%BLOCK_ID%% ",
        "tag": "run tag @s add %%PROJECT_NAME_LCF%%WillCraft%%CRAFT_NAME_UCF%%\n"
    },
    "clear_others": "execute as @e[type=minecraft:item,tag=%%PROJECT_NAME_LCF%%WillCraft%%CRAFT_NAME_UCF%%] at @s "
                    "run kill @e[type=minecraft:item,distance=..1,limit=1,"
                    "nbt={Item:{id:\"%%ID%%\",Count:%%COUNT%%b}}]\n",
    "run_func": "execute as @e[type=minecraft:item,tag=%%PROJECT_NAME_LCF%%WillCraft%%CRAFT_NAME_UCF%%] at @s "
                "run function hrt:items/%%CRAFT_NAME%%\n",
    "clear_self": "execute as @e[type=minecraft:item,tag=%%PROJECT_NAME_LCF%%WillCraft%%CRAFT_NAME_UCF%%] at @s "
                  "run kill @s\n",
    "gen_item": "summon minecraft:item ~ ~ ~ "
                "{Item:{id:\"%%ID%%\",Count:%%COUNT%%b,"
                "tag:{id:\"%%MOD_ID%%\","
                "display:{Name:'%%NAME%%',Lore:'%%LORE%%'}}}}"
}