#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from datetime import datetime
from nova_act import NovaAct
from pydantic import BaseModel

class ActResults(BaseModel):
    actProcessEnglishExplanation: str
    actResultEnglishExplanation: str


def run_test():
    # ログの設定
    log_file = f"nova_act_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    

    logging.info("=== Nova Act テスト実行開始 ===")
    start_time = datetime.now()
    
    results = []

    nova = NovaAct(starting_page="http://localhost:5173/", 
               ignore_https_errors=True, 
               headless=True,
               )
    
    # 各actの実行と結果の収集
    tasks = [
        "FlexMatch JSON ルールをロードするボタンをクリックして",
        "いずれかのルールを選択して",
        "OKを押して JSON をロードして",
        "Visualize ボタンを押して",
        "表示されたルールの名前とチーム構造を確認して"
    ]

    nova.start()
    for i, prompt in enumerate(tasks, 1):
        logging.info(f"タスク {i}: {prompt}")
        result = nova.act(prompt, schema=ActResults.model_json_schema())
        
        # 結果をログに記録
        logging.info(f"完了: ステップ数={result.metadata.num_steps_executed}")
        logging.info(f"応答: {result.response.actProcessEnglishExplanation}")
        
        results.append({
            "task": i,
            "prompt": prompt,
            "response": result.response,
            "steps": result.metadata.num_steps_executed,
            "act_id": result.metadata.act_id
        })





    
    # 実行完了
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # サマリーをファイルに出力
    summary_file = f"nova_act_summary.txt"

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(f"Nova Act 実行サマリー\n")
        f.write(f"日時: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"URL: http://localhost:5173/\n")
        f.write(f"タスク数: {len(tasks)}\n")
        f.write(f"合計時間: {duration:.2f}秒\n\n")
        
        for result in results:
            f.write(f"タスク {result['task']}: {result['prompt']}\n")
            f.write(f"ステップ数: {result['steps']}\n")
            f.write(f"応答: {result['response']}\n\n")
    
    logging.info(f"=== 実行完了 ===")
    logging.info(f"合計タスク数: {len(tasks)}")
    logging.info(f"合計実行時間: {duration:.2f}秒")
    logging.info(f"サマリーを {summary_file} に出力しました")
        
    return 0  # 成功



if __name__ == "__main__":
    print("Start Testing ")

    sys.exit(run_test())
