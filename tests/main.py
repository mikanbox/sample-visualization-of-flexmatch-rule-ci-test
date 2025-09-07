#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from nova_act import NovaAct

def run_test():

    nova = NovaAct(starting_page="http://localhost:5173/", 
               ignore_https_errors=True, 
               headless=True,
               )
    
    nova.start()
    nova.act("FlexMatch JSON ルールをロードするボタンをクリックして")
    nova.act("いずれかのルールを選択して")
    nova.act("OKを押して JSON をロードして")
    nova.act("Visualize ボタンを押して")

if __name__ == "__main__":
    print("Start Testing ")

    sys.exit(run_test())







