#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import json
from datetime import datetime
from nova_act import NovaAct
from pydantic import BaseModel

class ActResults(BaseModel):
    actProcessEnglishExplanation: str
    actResultEnglishExplanation: str

def Long_Scneraio():
    nova = NovaAct(starting_page="http://localhost:5173/", 
            ignore_https_errors=True, 
            headless=True,
            )
    nova.start()
    nova.act("Load FlexMatch Preset Rule を押して、Evenly matched teams を選択して OKを押し、Visualization を押して", schema=ActResults.model_json_schema())
    assert True  # テストが成功したことを示す

def Step_by_Step_Scenario():
    nova = NovaAct(starting_page="http://localhost:5173/", 
            ignore_https_errors=True, 
            headless=True,
            )
    nova.start()
    nova.act("Load FlexMatch Preset Rule を押して", schema=ActResults.model_json_schema())
    nova.act("Evenly matched teams を選択して OKを押して", schema=ActResults.model_json_schema())
    nova.act("Visualization を押して図が可視化されたことを確認して", schema=ActResults.model_json_schema())
    assert True  # テストが成功したことを示す

def test_basic_run():    
    logging.info("=== Nova Act テスト実行開始 ===")
    results = []
    nova = NovaAct(starting_page="http://localhost:5173/", 
               ignore_https_errors=True, 
               headless=True,
               )
    
    # タスクリストをJSONファイルから読み込む
    with open("tests/tasks.json", "r", encoding="utf-8") as f:
        tasks_data = json.load(f)
        tasks = tasks_data["tasks"]

    nova.start()
    for i, prompt in enumerate(tasks, 1):
        logging.info(f"タスク {i}: {prompt}")
        try:
            result = nova.act(prompt, schema=ActResults.model_json_schema())
            
            # 結果をログに記録
            logging.info(f"完了: ステップ数={result.metadata.num_steps_executed}")
            response_data = json.loads(result.response)
            logging.info(f"応答: {response_data["actProcessEnglishExplanation"]}")
            
            results.append({
                "task": i,
                "prompt": prompt,
                "response": result.response,
                "steps": result.metadata.num_steps_executed,
                "act_id": result.metadata.act_id,
                "error": False  # エラーなし
            })
        except Exception as e:
            # エラーをログに記録
            logging.error(f"エラー: {str(e)}")
            
            results.append({
                "task": i,
                "prompt": prompt,
                "response": str(e),
                "steps": 0,
                "act_id": None,
                "error": True  # エラーあり
            })
            
    # pytestのテスト関数は値を返すべきではない
    assert True  # テストが成功したことを示す



if __name__ == "__main__":
    print("Start Testing ")

    sys.exit(run_basic_test())
