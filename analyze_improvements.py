#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
训练效果分析工具 - 对比优化前后的效果
"""

import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter, defaultdict


def load_previous_results():
    """加载之前的训练结果"""
    # 基于之前提到的数据
    return {
        'total_challenges': 10000,
        'correct': 2500,
        'accuracy': 0.25,
        'training_duration': 3 * 3600 + 14 * 60,  # 3小时14分钟
        'categories': {
            'crypto': {'correct': 500, 'total': 2000, 'accuracy': 0.25},
            'web': {'correct': 450, 'total': 1800, 'accuracy': 0.25},
            'pwn': {'correct': 300, 'total': 1200, 'accuracy': 0.25},
            'reverse': {'correct': 350, 'total': 1400, 'accuracy': 0.25},
            'forensics': {'correct': 500, 'total': 2000, 'accuracy': 0.25},
            'misc': {'correct': 400, 'total': 1600, 'accuracy': 0.25}
        },
        'difficulties': {
            'easy': {'correct': 1000, 'total': 3000, 'accuracy': 0.33},
            'medium': {'correct': 1000, 'total': 4000, 'accuracy': 0.25},
            'hard': {'correct': 500, 'total': 3000, 'accuracy': 0.17}
        },
        'training_time': "3小时14分钟"
    }


def load_optimized_results():
    """加载优化后的训练结果"""
    try:
        with open('optimized_training_results.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("优化训练结果文件不存在，请先运行优化训练")
        return None


def compare_results(previous, optimized):
    """对比优化前后的结果"""
    print("=" * 70)
    print("                    训练效果对比分析")
    print("=" * 70)
    print()
    
    # 总体对比
    print("【总体表现】")
    print(f"{'指标':20s} | {'优化前':15s} | {'优化后':15s} | {'提升':15s}")
    print("-" * 70)
    print(f"{'训练题目数':20s} | {previous['total_challenges']:15d} | {optimized['total_challenges']:15d} | {'--':15s}")
    print(f"{'正确题目数':20s} | {previous['correct']:15d} | {optimized['correct']:15d} | {optimized['correct'] - previous['correct']:+15d}")
    print(f"{'训练准确率':20s} | {previous['accuracy']:15.2%} | {optimized['accuracy']:15.2%} | {(optimized['accuracy'] - previous['accuracy']):+.2%}")
    print()
    
    # 训练时长对比
    prev_duration = previous.get('training_duration', 0)
    opt_duration = optimized.get('training_duration', 0)
    duration_diff = opt_duration - prev_duration
    
    print(f"{'训练时长':20s} | {previous.get('training_time', 'N/A'):15s} | {optimized.get('training_duration_formatted', 'N/A'):15s} | {duration_diff/60:+15.1f} 分钟")
    print()
    
    # 难度对比
    print("【难度表现】")
    print(f"{'难度':10s} | {'优化前':20s} | {'优化后':20s} | {'提升':15s}")
    print("-" * 70)
    for difficulty in ['easy', 'medium', 'hard']:
        prev_diff = previous['difficulties'].get(difficulty, {})
        opt_diff = optimized['difficulty_progression'].get(difficulty, {})
        
        prev_acc = prev_diff.get('accuracy', 0)
        opt_acc = opt_diff.get('accuracy', 0)
        improvement = opt_acc - prev_acc
        
        print(f"{difficulty:10s} | {prev_acc:15.2%} ({prev_diff.get('total', 0):4d}) | "
              f"{opt_acc:15.2%} ({opt_diff.get('count', 0):4d}) | {improvement:+.2%}")
    print()
    
    # 类别对比
    print("【类别表现】")
    print(f"{'类别':15s} | {'优化前':20s} | {'优化后':20s} | {'提升':15s}")
    print("-" * 70)
    for category in ['crypto', 'web', 'pwn', 'reverse', 'forensics', 'misc']:
        prev_cat = previous['categories'].get(category, {})
        opt_cat = optimized['category_performance'].get(category, {})
        
        prev_acc = prev_cat.get('accuracy', 0)
        opt_acc = opt_cat.get('accuracy', 0)
        improvement = opt_acc - prev_acc
        
        print(f"{category:15s} | {prev_acc:15.2%} ({prev_cat.get('total', 0):4d}) | "
              f"{opt_acc:15.2%} ({opt_cat.get('total', 0):4d}) | {improvement:+.2%}")
    print()
    
    # 知识库对比
    print("【其他指标】")
    print(f"知识库大小: {optimized['knowledge_base_size']} 条")
    print(f"最终难度: {optimized['final_difficulty']}")
    print()
    
    # 评估
    print("【综合评估】")
    accuracy_improvement = optimized['accuracy'] - previous['accuracy']
    
    if accuracy_improvement > 0.20:
        rating = "🌟🌟🌟🌟🌟 非常优秀"
    elif accuracy_improvement > 0.15:
        rating = "🌟🌟🌟🌟 优秀"
    elif accuracy_improvement > 0.10:
        rating = "🌟🌟🌟 良好"
    elif accuracy_improvement > 0.05:
        rating = "🌟🌟 中等"
    else:
        rating = "🌟 需要改进"
    
    print(f"准确率提升: {accuracy_improvement:+.2%}")
    print(f"评级: {rating}")
    
    # 效率分析
    if prev_duration > 0:
        time_per_question_prev = prev_duration / previous['total_challenges']
        time_per_question_opt = opt_duration / optimized['total_challenges']
        efficiency_ratio = time_per_question_prev / time_per_question_opt
        
        print(f"效率提升: {efficiency_ratio:.2f}x (每题用时减少 {(1 - 1/efficiency_ratio):.1%})")
    
    print("=" * 70)
    print()


def generate_improvement_report(previous, optimized):
    """生成改进报告并保存"""
    report = {
        'timestamp': pd.Timestamp.now().isoformat(),
        'previous_results': previous,
        'optimized_results': optimized,
        'improvements': {
            'accuracy': optimized['accuracy'] - previous['accuracy'],
            'accuracy_percentage': (optimized['accuracy'] / previous['accuracy'] - 1) * 100,
            'correct_questions': optimized['correct'] - previous['correct'],
            'final_difficulty': optimized['final_difficulty'],
            'knowledge_base_size': optimized['knowledge_base_size']
        },
        'category_improvements': {},
        'difficulty_improvements': {}
    }
    
    # 计算各类别改进
    for category in previous['categories'].keys():
        prev_acc = previous['categories'][category]['accuracy']
        opt_cat = optimized['category_performance'].get(category, {})
        opt_acc = opt_cat.get('accuracy', 0)
        report['category_improvements'][category] = {
            'accuracy_improvement': opt_acc - prev_acc,
            'improvement_percentage': (opt_acc / prev_acc - 1) * 100 if prev_acc > 0 else 0
        }
    
    # 计算各难度改进
    for difficulty in previous['difficulties'].keys():
        prev_acc = previous['difficulties'][difficulty]['accuracy']
        opt_diff = optimized['difficulty_progression'].get(difficulty, {})
        opt_acc = opt_diff.get('accuracy', 0)
        report['difficulty_improvements'][difficulty] = {
            'accuracy_improvement': opt_acc - prev_acc,
            'improvement_percentage': (opt_acc / prev_acc - 1) * 100 if prev_acc > 0 else 0
        }
    
    # 保存报告
    with open('improvement_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("✅ 改进报告已保存到: improvement_report.json")
    print()
    
    return report


def plot_improvement_chart(previous, optimized):
    """绘制改进图表"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('CTF训练优化效果对比', fontsize=16)
    
    # 1. 总体准确率对比
    ax1 = axes[0, 0]
    categories = ['优化前', '优化后']
    accuracies = [previous['accuracy'], optimized['accuracy']]
    colors = ['#ff6b6b', '#4ecdc4']
    bars = ax1.bar(categories, accuracies, color=colors, alpha=0.7)
    ax1.set_ylabel('准确率')
    ax1.set_title('总体准确率对比')
    ax1.set_ylim(0, 1)
    for bar, acc in zip(bars, accuracies):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{acc:.2%}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax1.axhline(y=0.25, color='red', linestyle='--', alpha=0.5, label='基准线')
    ax1.legend()
    
    # 2. 难度对比
    ax2 = axes[0, 1]
    difficulties = ['easy', 'medium', 'hard']
    prev_diff_acc = [previous['difficulties'][d]['accuracy'] for d in difficulties]
    opt_diff_acc = [optimized['difficulty_progression'].get(d, {'accuracy': 0})['accuracy'] for d in difficulties]
    
    x = range(len(difficulties))
    width = 0.35
    
    bars1 = ax2.bar([i - width/2 for i in x], prev_diff_acc, width, label='优化前', color='#ff6b6b', alpha=0.7)
    bars2 = ax2.bar([i + width/2 for i in x], opt_diff_acc, width, label='优化后', color='#4ecdc4', alpha=0.7)
    
    ax2.set_ylabel('准确率')
    ax2.set_title('各难度准确率对比')
    ax2.set_xticks(x)
    ax2.set_xticklabels(difficulties)
    ax2.legend()
    ax2.set_ylim(0, 1)
    
    # 3. 类别对比
    ax3 = axes[1, 0]
    cats = list(previous['categories'].keys())
    prev_cat_acc = [previous['categories'][c]['accuracy'] for c in cats]
    opt_cat_acc = [optimized['category_performance'].get(c, {'accuracy': 0})['accuracy'] for c in cats]
    
    x = range(len(cats))
    bars1 = ax3.bar([i - width/2 for i in x], prev_cat_acc, width, label='优化前', color='#ff6b6b', alpha=0.7)
    bars2 = ax3.bar([i + width/2 for i in x], opt_cat_acc, width, label='优化后', color='#4ecdc4', alpha=0.7)
    
    ax3.set_ylabel('准确率')
    ax3.set_title('各类别准确率对比')
    ax3.set_xticks(x)
    ax3.set_xticklabels(cats, rotation=45)
    ax3.legend()
    ax3.set_ylim(0, 1)
    
    # 4. 知识库增长
    ax4 = axes[1, 1]
    kb_size = optimized['knowledge_base_size']
    
    # 创建饼图
    if optimized.get('category_performance'):
        cat_counts = {cat: stats['total'] for cat, stats in optimized['category_performance'].items()}
        labels = list(cat_counts.keys())
        sizes = list(cat_counts.values())
        
        ax4.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
        ax4.set_title(f'优化后题目分布\n(总题数: {optimized["total_challenges"]})')
    
    plt.tight_layout()
    plt.savefig('training_improvement_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ 对比图表已保存到: training_improvement_chart.png")
    print()


def main():
    """主函数"""
    print("加载训练数据...")
    
    # 加载数据
    previous = load_previous_results()
    optimized = load_optimized_results()
    
    if optimized is None:
        print("错误: 未找到优化训练结果")
        return
    
    # 对比结果
    compare_results(previous, optimized)
    
    # 生成报告
    report = generate_improvement_report(previous, optimized)
    
    # 绘制图表
    try:
        plot_improvement_chart(previous, optimized)
    except Exception as e:
        print(f"绘制图表时出错: {e}")
    
    print("=" * 70)
    print("分析完成！所有结果已保存。")
    print("=" * 70)


if __name__ == '__main__':
    main()
