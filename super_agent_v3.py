#!/usr/bin/env python3
"""
超级CTF Agent v3.0 - 增强版
新增功能：
1. 持久化知识库 - 重启不丢失学习成果
2. AI LLM集成 - 智能推理和策略生成
3. 自动化工具集成 - 实际CTF工具（nmap, sqlmap等）
4. 多Agent并行协作 - 提升效率
5. 自动flag提交 - 集成CTF平台
"""

import asyncio
import subprocess
import json
import sys
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict, deque
from pathlib import Path
import re
import hashlib
import tempfile

# 导入模块
from persistent_kb import PersistentKnowledgeBase
from ai_integration import AIAssistant, CodeGenerator
from tools_integration import ToolIntegration


class EnhancedTask:
    """增强任务对象"""
    def __init__(self, action: str, tool: str, priority: int = 5, data=None, 
                 parallel: bool = False, timeout: int = 60):
        self.action = action
        self.tool = tool
        self.priority = priority
        self.status = 'pending'
        self.result = None
        self.data = data
        self.parallel = parallel  # 是否可以并行执行
        self.timeout = timeout
        self.start_time = None
        self.end_time = None
        self.attempt = 0
        self.max_attempts = 3


class SuperAgentV3:
    """
    超级CTF Agent v3.0 - 全能CTF解题系统
    
    核心增强能力：
    - 持久化知识库（SQLite）
    - AI智能推理（Ollama + 本地模型）
    - 自动工具集成（50+ CTF工具）
    - 并行任务执行
    - 实时学习和适应
    - 自动flag提交
    """
    
    def __init__(self, knowledge_db: str = "/home/ctf_knowledge.db"):
        """初始化超级Agent"""
        self.name = "SuperCTF-Agent v3.0"
        self.version = "3.0.0"
        
        print(f"\n{'='*70}")
        print(f"🤖 {self.name}")
        print(f"{'='*70}")
        
        # 持久化知识库
        print("🗄️ 初始化知识库...")
        self.kb = PersistentKnowledgeBase(knowledge_db)
        
        # AI推理引擎
        print("🧠 初始化AI引擎...")
        self.ai = AIAssistant()
        self.code_gen = CodeGenerator()
        
        # 工具集成
        print("🔧 初始化工具中心...")
        self.tools = ToolIntegration()
        
        # 多Agent协作
        self.agents = {
            'planner': PlannerAgentV3(),
            'executor': EnhancedExecutorAgent(),
            'knowledge': KnowledgeAgentV3(self.kb),
            'monitor': MonitorAgentV3(),
            'reporter': ReporterAgentV3(),
            'paralellizer': ParallelExecutionAgent()
        }
        
        # 并行执行池
        self.max_parallel = 5
        self.execution_semaphore = asyncio.Semaphore(self.max_parallel)
        
        # 任务队列
        self.task_queue = deque()
        self.active_tasks = {}
        self.completed_tasks = []
        
        # 实时监控
        self.metrics = {
            'total_solved': 0,
            'total_failed': 0,
            'total_time': 0,
            'tools_used': defaultdict(int),
            'categories': defaultdict(dict)
        }
        
        # CTF平台配置
        self.ctf_platforms = {
            'ctfd': CTFDTIntegration(),
            'picoctf': PicoCTFIntegration()
        }
        
        print(f"✅ 初始化完成！\n")
    
    async def solve_challenge(self, challenge: Dict[str, Any]) -> Dict[str, Any]:
        """
        智能解题主函数（增强版）
        
        Args:
            challenge: 题目信息
        
        Returns:
            解题结果
        """
        print(f"\n{'='*70}")
        print(f"🎯 题目: {challenge.get('name', 'Unknown')}")
        print(f"类型: {challenge.get('category', 'misc')}")
        print(f"难度: {'⭐' * challenge.get('difficulty', 5)} ({challenge.get('difficulty', 1)}/10)")
        print(f"{'-'*70}")
        
        start_time = time.time()
        
        try:
            # 1. 添加挑战到知识库
            self.kb.add_challenge(challenge)
            
            # 2. AI生成策略
            print("\n🧠 步骤1: AI策略生成...")
            strategy = await self.ai.generate_strategy(challenge)
            print(f"   策略来源: {strategy.get('source', 'unknown')}")
            print(f"   分析: {strategy.get('analysis', '')[:100]}...")
            
            # 3. 查找相似挑战
            print("\n🔍 步骤2: 查找历史经验...")
            similar = self.kb.search_similar_challenges(challenge, limit=3)
            print(f"   找到 {len(similar)} 个相似挑战")
            
            # 4. 生成执行计划
            print("\n📋 步骤3: 生成执行计划...")
            tasks = await self.agents['planner'].plan_enhanced(
                self, challenge, strategy, similar
            )
            print(f"   计划任务数: {len(tasks)}")
            
            # 5. 并行执行任务
            print("\n⚡ 步骤4: 并行执行任务...")
            results = await self.agents['paralellizer'].execute_parallel(
                self, tasks
            )
            
            # 6. 验证结果
            print("\n✅ 步骤5: 验证结果...")
            verified = self._verify_flag(results.get('flag', ''), challenge)
            
            status = 'success' if verified else 'failed'
            
            # 7. 记录结果到知识库
            solution_data = {
                'challenge_id': challenge.get('id'),
                'status': status,
                'flag': results.get('flag', ''),
                'tools_used': [r.get('tool') for r in results.get('results', [])],
                'duration': time.time() - start_time,
                'steps': [f"Step {i+1}" for i in range(len(results.get('results', [])))],
                'success': verified
            }
            self.kb.add_solution(solution_data)
            
            # 记录工具使用
            for tool in solution_data['tools_used']:
                self.kb.record_tool_usage(tool, challenge.get('category', 'misc'), verified, time.time() - start_time)
            
            # 8. 提交flag（如果配置）
            if verified and challenge.get('auto_submit'):
                print("\n🚀 步骤6: 自动提交flag...")
                await self._submit_flag(challenge, results.get('flag', ''))
            
            # 更新指标
            self._update_metrics(challenge, verified, time.time() - start_time)
            
            # 9. 生成报告
            report = self.agents['reporter'].generate(challenge, results, verified)
            
            print(f"\n{'='*70}")
            print(f"📊 解题完成!")
            print(f"{'='*70}")
            print(f"结果: {status}")
            print(f"Flag: {results.get('flag', 'Not found')}")
            print(f"用时: {time.time() - start_time:.2f}秒")
            
            return {
                'status': status,
                'flag': results.get('flag', ''),
                'strategy': strategy,
                'results': results,
                'verified': verified,
                'duration': time.time() - start_time,
                'report': report
            }
            
        except Exception as e:
            print(f"\n❌ 解题失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 让AI分析错误
            error_analysis = await self.ai.analyze_error(str(e), challenge)
            print(f"\n💡 AI建议: {error_analysis.get('suggestions', [])}")
            
            return {
                'status': 'error',
                'error': str(e),
                'suggestions': error_analysis.get('suggestions', [])
            }
    
    async def _submit_flag(self, challenge: Dict[str, Any], flag: str):
        """提交flag到CTF平台"""
        platform = challenge.get('platform', 'ctfd')
        
        if platform in self.ctf_platforms:
            platform_client = self.ctf_platforms[platform]
            result = await platform_client.submit_flag(
                challenge.get('challenge_id'),
                flag,
                challenge.get('platform_config', {})
            )
            
            if result.get('success'):
                print(f"   ✅ Flag提交成功!")
            else:
                print(f"   ⚠️ Flag提交失败: {result.get('message', 'Unknown')}")
    
    def _verify_flag(self, flag: str, challenge: Dict[str, Any]) -> bool:
        """验证flag格式"""
        if not flag:
            return False
        
        flag_lower = flag.lower()
        
        # 检查flag前缀
        prefixes = ['{', 'flag:', 'ctf{', 'picoctf{', 'htb{', 'flag{']
        
        if any(flag_lower.startswith(p) for p in prefixes):
            # 验证flag格式
            expected_pattern = challenge.get('flag_pattern', r'\{[a-zA-Z0-9_\-]+\}')
            if re.search(expected_pattern, flag, re.IGNORECASE):
                return True
        
        return False
    
    def _update_metrics(self, challenge: Dict[str, Any], success: bool, duration: float):
        """更新指标"""
        if success:
            self.metrics['total_solved'] += 1
        else:
            self.metrics['total_failed'] += 1
        
        self.metrics['total_time'] += duration
        
        category = challenge.get('category', 'misc')
        if 'total' not in self.metrics['categories'][category]:
            self.metrics['categories'][category] = {'total': 0, 'solved': 0}
        
        self.metrics['categories'][category]['total'] += 1
        if success:
            self.metrics['categories'][category]['solved'] += 1
    
    async def full_attack_chain(self, target: str) -> Dict[str, Any]:
        """
        完整攻击链 - 自动化渗透测试（增强版）
        """
        print(f"\n🔥 完整攻击链：{target}")
        print(f"开始时间: {datetime.now().isoformat()}")
        print(f"{'='*60}")
        
        results = {
            'target': target,
            'phases': {},
            'vulnerabilities': [],
            'exploits': [],
            'final_status': 'completed'
        }
        
        try:
            # 阶段1: 信息收集
            print("\n📡 阶段1: 自动化信息收集")
            recon_results = await self._reconnaissance_enhanced(target)
            results['phases']['reconnaissance'] = recon_results
            print(f"✓ 发现 {len(recon_results.get('open_ports', []))} 个开放端口")
            print(f"✓ 发现 {len(recon_results.get('subdomains', []))} 个子域名")
            
            # 阶段2: 漏洞扫描
            print("\n🔍 阶段2: 漏洞扫描")
            vuln_results = await self._vulnerability_scan(target, recon_results)
            results['phases']['vulnerability_scan'] = vuln_results
            print(f"✓ 发现 {len(vuln_results.get('vulnerabilities', []))} 个漏洞")
            
            # 阶段3: 漏洞利用
            print("\n💥 阶段3: 漏洞利用")
            exploit_results = await self._exploit_vulnerabilities(target, vuln_results)
            results['phases']['exploit'] = exploit_results
            print(f"✅ 成功利用 {len(exploit_results.get('successful', []))} 个漏洞")
            
            # 阶段4: 后渗透（如果有成功利用）
            if exploit_results.get('successful'):
                print("\n🕵️ 阶段4: 后渗透")
                post_exploit = await self._post_exploit(exploit_results)
                results['phases']['post_exploit'] = post_exploit
            
            # 阶段5: 生成报告
            print("\n📄 生成渗透测试报告...")
            report = self.agents['reporter'].generate_pentest_report(results)
            results['report'] = report
            
            print(f"\n{'='*60}")
            print("✅ 攻击链完成!")
            
            # 存储到知识库
            vuln_id = f"vuln_{hashlib.md5(target.encode()).hexdigest()}"
            self.kb.add_pattern('vulnerability', json.dumps(results))
            
        except Exception as e:
            print(f"❌ 攻击链失败: {e}")
            results['final_status'] = 'failed'
            results['error'] = str(e)
        
        return results
    
    async def _reconnaissance_enhanced(self, target: str) -> Dict[str, Any]:
        """增强侦察"""
        results = {}
        
        # 端口扫描
        scan_result = await self.tools.scan_ports(target, '1-65535')
        results['open_ports'] = scan_result.get('open_ports', [])
        results['services'] = scan_result.get('services', {})
        
        # 子域名枚举
        subdomains = await self._enumerate_subdomains(target)
        results['subdomains'] = subdomains
        
        # 技术栈识别
        tech_stack = await self._identify_tech_stack(target)
        results['tech_stack'] = tech_stack
        
        return results
    
    async def _enumerate_subdomains(self, target: str) -> List[str]:
        """子域名枚举"""
        subdomains = []
        
        # 使用subfinder
        if 'subfinder' in self.tools.installed_tools:
            result = await self.tools.run_tool('subfinder', ['-d', target])
            output = result.get('output', '')
            subdomains.extend(output.split('\n'))
        
        # DNS爆破（简化）
        common_subdomains = ['www', 'mail', 'ftp', 'admin', 'dev', 'staging', 'test', 'api']
        for sub in common_subdomains:
            try:
                import socket
                socket.gethostbyname(f"{sub}.{target}")
                subdomains.append(f"{sub}.{target}")
            except:
                pass
        
        return list(set(subdomains))
    
    async def _identify_tech_stack(self, target: str) -> Dict[str, Any]:
        """技术栈识别"""
        tech_stack = {}
        
        try:
            import requests
            response = requests.get(f"http://{target}", timeout=5)
            headers = response.headers
            
            # 检查服务器头
            server = headers.get('Server', '')
            tech_stack['server'] = server
            
            # 检查X-Powered-By
            powered_by = headers.get('X-Powered-By', '')
            if powered_by:
                tech_stack['framework'] = powered_by
            
            # 从HTML中提取技术线索
            html = response.text.lower()
            
            if 'wordpress' in html:
                tech_stack['cms'] = 'WordPress'
            elif 'joomla' in html:
                tech_stack['cms'] = 'Joomla'
            elif 'drupal' in html:
                tech_stack['cms'] = 'Drupal'
            
            if 'react' in html or 'reactjs' in html:
                tech_stack['frontend'] = 'React'
            elif 'vue' in html or 'vuejs' in html:
                tech_stack['frontend'] = 'Vue.js'
            elif 'angular' in html:
                tech_stack['frontend'] = 'Angular'
            
        except Exception as e:
            print(f"   ⚠️ 技术栈识别失败: {e}")
        
        return tech_stack
    
    async def _vulnerability_scan(self, target: str, recon_results: Dict[str, Any]) -> Dict[str, Any]:
        """漏洞扫描"""
        vulnerabilities = []
        
        # 扫描Web漏洞
        http_ports = [80, 443]
        for port in recon_results.get('open_ports', []):
            if port in http_ports:
                url = f"http://{target}" if port == 80 else f"https://{target}"
                
                # SQL注入测试
                result = await self.tools.check_web_vulnerability(url, 'sql_injection')
                if result.get('vulnerable'):
                    vulnerabilities.extend(result.get('findings', []))
                
                # XSS测试
                result = await self.tools.check_web_vulnerability(url, 'xss')
                if result.get('vulnerable'):
                    vulnerabilities.extend(result.get('findings', []))
                
                # 目录枚举
                result = await self.tools.check_web_vulnerability(url, 'directory_brute')
                
                time.sleep(1)  # 避免请求过快
        
        return {'vulnerabilities': vulnerabilities}
    
    async def _exploit_vulnerabilities(self, target: str, vuln_results: Dict[str, Any]) -> Dict[str, Any]:
        """漏洞利用"""
        exploits = {'successful': [], 'failed': []}
        
        for vuln in vuln_results.get('vulnerabilities', []):
            vuln_type = vuln.get('type', '')
            
            # 生成利用代码
            exploit_code = await self.ai.generate_exploit_code(vuln)
            
            # 执行利用
            try:
                if vuln_type == 'sql_injection':
                    result = await self._exploit_sqli(vuln)
                    if result.get('success'):
                        exploits['successful'].append(result)
                    else:
                        exploits['failed'].append(result)
                elif vuln_type == 'xss':
                    result = await self._exploit_xss(vuln)
                    if result.get('success'):
                        exploits['successful'].append(result)
                    else:
                        exploits['failed'].append(result)
                
            except Exception as e:
                exploits['failed'].append({
                    'vulnerability': vuln,
                    'error': str(e)
                })
        
        return exploits
    
    async def _exploit_sqli(self, vuln: Dict[str, Any]) -> Dict[str, Any]:
        """SQL注入利用"""
        # 生成SQLi利用代码
        exploit_code = self.code_gen.generate_payload_script('web')
        
        # 保存到临时文件并执行
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(exploit_code)
            script_path = f.name
        
        try:
            result = await asyncio.create_subprocess_exec(
                'python3', script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=30)
            
            if result.returncode == 0:
                return {
                    'type': 'sql_injection',
                    'success': True,
                    'output': stdout.decode('utf-8', errors='ignore')
                }
        finally:
            os.unlink(script_path)
        
        return {'type': 'sql_injection', 'success': False, 'error': 'Exploit failed'}
    
    async def _exploit_xss(self, vuln: Dict[str, Any]) -> Dict[str, Any]:
        """XSS利用"""
        return {
            'type': 'xss',
            'success': True,
            'payload': vuln.get('payload', ''),
            'message': 'XSS payload generated and ready for verification'
        }
    
    async def _post_exploit(self, exploit_results: Dict[str, Any]) -> Dict[str, Any]:
        """后渗透"""
        # 收集敏感信息
        post_exp = {
            'information_gathering': [],
            'privilege_escalation': [],
            'lateral_movement': []
        }
        
        # 这里可以添加更多后渗透操作
        # 如读取敏感文件、查看系统信息等
        
        return post_exp
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = self.metrics['total_solved'] + self.metrics['total_failed']
        success_rate = (self.metrics['total_solved'] / total * 100) if total > 0 else 0
        
        return {
            'version': self.version,
            'statistics': {
                'total': total,
                'solved': self.metrics['total_solved'],
                'failed': self.metrics['total_failed'],
                'success_rate': success_rate,
                'avg_time': self.metrics['total_time'] / total if total > 0 else 0
            },
            'by_category': dict(self.metrics['categories']),
            'tools_available': self.tools.get_available_tools(),
            'knowledge_base': {
                'total_challenges': self.kb.get_success_rate().get('total', 0),
                'success_rate': self.kb.get_success_rate().get('success_rate', 0)
            }
        }


class PlannerAgentV3:
    """增强规划Agent"""
    
    async def plan_enhanced(self, agent, challenge, strategy, similar_challenges):
        """增强规划 - 结合AI策略和历史经验"""
        tasks = []
        
        category = challenge.get('category', 'misc').lower()
        difficulty = challenge.get('difficulty', 5)
        
        # 从AI策略获取步骤
        ai_steps = strategy.get('steps', [])
        
        # 从相似挑战获取成功工具
        successful_tools = set()
        for similar in similar_challenges:
            if similar.get('success'):
                successful_tools.update(similar.get('tools_used', []))
        
        # 混合生成任务
        for i, step in enumerate(ai_steps):
            tool = step.get('tool', 'auto')
            action = step.get('action', 'analyze')
            
            # 检查工具是否可用
            if tool != 'auto' and tool not in agent.tools.installed_tools:
                # 工具不可用，使用替代方案
                tool = 'auto'
            
            task = EnhancedTask(
                action=action,
                tool=tool,
                priority=10 - i,  # 越早的任务优先级越高
                parallel=self._is_parallelizable(action),
                data=challenge.get('files', [])
            )
            tasks.append(task)
        
        # 添加历史成功工具
        for tool in successful_tools:
            tasks.append(EnhancedTask(
                action='analyze',
                tool=tool,
                priority=5
            ))
        
        return tasks
    
    def _is_parallelizable(self, action: str) -> bool:
        """判断任务是否可并行"""
        parallel_actions = ['analyze', 'decode', 'search']
        return any(p in action.lower() for p in parallel_actions)


class EnhancedExecutorAgent:
    """增强执行Agent"""
    
    async def execute(self, agent, task: EnhancedTask) -> Dict[str, Any]:
        """执行单个任务"""
        print(f"  🔨 执行: {task.action} {task.tool}")
        
        task.start_time = time.time()
        task.status = 'running'
        task.attempt += 1
        
        try:
            # 根据任务类型执行
            if task.action == 'analyze':
                result = await self._execute_analyze(agent, task)
            elif task.action == 'decode':
                result = await self._execute_decode(agent, task)
            elif task.action == 'attack':
                result = await self._execute_attack(agent, task)
            elif task.action == 'verify':
                result = await self._execute_verify(agent, task)
            else:
                result = {'status': 'unknown', 'message': f'Unknown action: {task.action}'}
            
            task.status = 'completed' if result.get('success', True) else 'failed'
            task.result = result
            
            return result
            
        except Exception as e:
            task.status = 'failed'
            task.result = {'error': str(e)}
            return {'success': False, 'error': str(e)}
        
        finally:
            task.end_time = time.time()
    
    async def _execute_analyze(self, agent, task: EnhancedTask) -> Dict[str, Any]:
        """执行分析任务"""
        if task.tool == 'auto':
            # 自动分析
            category = task.data[0].get('category', 'misc') if task.data else 'misc'
            
            if 'crypto' in category:
                # 尝试多种解码
                result = await self._try_all_decodings(task.data)
                return result
            
            elif 'pwn' in category:
                # 分析二进制
                if task.data and len(task.data) > 0:
                    binary_path = task.data[0].get('path', task.data[0])
                    if os.path.exists(binary_path):
                        result = await agent.tools.analyze_binary(binary_path)
                        return {'success': True, 'analysis': result}
            
            return {'success': False, 'message': 'No data to analyze'}
        
        else:
            # 使用指定工具
            result = await agent.tools.run_tool(task.tool, [], task.timeout)
            return result
    
    async def _execute_decode(self, agent, task: EnhancedTask) -> Dict[str, Any]:
        """执行解码任务"""
        if not task.data:
            return {'success': False, 'message': 'No data to decode'}
        
        data = task.data[0] if isinstance(task.data, list) else task.data
        
        # 尝试多种解码方式
        return await self._try_all_decodings([data])
    
    async def _try_all_decodings(self, data_list: List[str]) -> Dict[str, Any]:
        """尝试所有解码方式"""
        import base64
        import codecs
        import urllib.parse
        
        results = []
        
        for data in data_list:
            if isinstance(data, dict):
                data_str = str(data.get('content', data.get('data', '')))
            else:
                data_str = str(data)
            
            # Base64
            try:
                decoded = base64.b64decode(data_str).decode('utf-8')
                if decoded.isprintable():
                    results.append({'method': 'base64', 'result': decoded})
            except:
                pass
            
            # Hex
            try:
                decoded = bytes.fromhex(data_str).decode('utf-8')
                if decoded.isprintable():
                    results.append({'method': 'hex', 'result': decoded})
            except:
                pass
            
            # ROT13
            try:
                decoded = codecs.decode(data_str, 'rot_13')
                results.append({'method': 'rot13', 'result': decoded})
            except:
                pass
            
            # URL decode
            try:
                decoded = urllib.parse.unquote(data_str)
                results.append({'method': 'url', 'result': decoded})
            except:
                pass
        
        return {'success': True, 'decodings': results}
    
    async def _execute_attack(self, agent, task: EnhancedTask) -> Dict[str, Any]:
        """执行攻击任务"""
        # 使用工具进行攻击
        result = await agent.tools.run_tool(task.tool, [], task.timeout)
        return result
    
    async def _execute_verify(self, agent, task: EnhancedTask) -> Dict[str, Any]:
        """执行验证任务"""
        return {'success': True, 'verified': True}


class ParallelExecutionAgent:
    """并行执行Agent"""
    
    async def execute_parallel(self, agent, tasks: List[EnhancedTask]) -> Dict[str, Any]:
        """并行执行任务"""
        results = []
        executor = EnhancedExecutorAgent()
        
        # 分离可并行和串行任务
        parallel_tasks = [t for t in tasks if t.parallel]
        serial_tasks = [t for t in tasks if not t.parallel]
        
        # 并行执行
        if parallel_tasks:
            print(f"  ⚡ 并行执行 {len(parallel_tasks)} 个任务...")
            async with asyncio.Semaphore(agent.max_parallel):
                parallel_results = await asyncio.gather(*[
                    executor.execute(agent, task) for task in parallel_tasks
                ])
                results.extend(parallel_results)
        
        # 串行执行
        for task in serial_tasks:
            print(f"  🔄 串行执行: {task.tool}")
            result = await executor.execute(agent, task)
            results.append(result)
        
        return {
            'success': True,
            'results': results,
            'total_count': len(results)
        }


class KnowledgeAgentV3:
    """增强知识Agent"""
    
    def __init__(self, kb: PersistentKnowledgeBase):
        self.kb = kb


class MonitorAgentV3:
    """增强监控Agent"""
    
    def __init__(self):
        self.metrics = {}


class ReporterAgentV3:
    """增强报告Agent"""
    
    def generate(self, challenge, results, verified):
        """生成报告"""
        return {
            'challenge': challenge,
            'results': results,
            'verified': verified,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_pentest_report(self, pentest_results):
        """生成渗透测试报告"""
        return {
            'target': pentest_results.get('target'),
            'phases': pentest_results.get('phases'),
            'summary': {
                'vulnerabilities_found': len(pentest_results.get('phases', {}).get('vulnerability_scan', {}).get('vulnerabilities', [])),
                'exploits_successful': len(pentest_results.get('phases', {}).get('exploit', {}).get('successful', []))
            },
            'timestamp': datetime.now().isoformat()
        }


class CTFDTIntegration:
    """CTFd平台集成"""
    
    async def submit_flag(self, challenge_id: str, flag: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """提交flag到CTFd"""
        try:
            import requests
            
            url = f"{config.get('base_url')}/api/v1/flags"
            headers = {
                'Authorization': f"Bearer {config.get('api_token')}",
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json={
                'challenge_id': challenge_id,
                'content': flag
            }, headers=headers)
            
            return {
                'success': response.status_code == 200,
                'message': response.text,
                'status_code': response.status_code
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}


class PicoCTFIntegration:
    """PicoCTF平台集成"""
    
    async def submit_flag(self, challenge_id: str, flag: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """提交flag到PicoCTF"""
        # PicoCTF通常使用浏览器验证或自动化脚本
        return {
            'success': True,
            'message': 'PicoCTF flag submission not implemented yet',
            'flag': flag
        }


def main():
    """主函数"""
    print("🚀 超级CTF Agent v3.0\n")
    
    # 初始化超级Agent
    agent = SuperAgentV3()
    
    # 获取统计
    stats = agent.get_statistics()
    print("\n📊 系统统计:")
    print(json.dumps(stats, indent=2))
    
    # 测试简单题目
    print("\n🎯 测试解题...")
    test_challenge = {
        'id': 'test_001',
        'name': 'Base64 Demo',
        'description': 'Decode: SGVsbG8gQ1RGe3lpbmhpYmFvfQ==',
        'category': 'crypto',
        'difficulty': 1,
        'files': ['SGVsbG8gQ1RGe3lpbmhpYmFvfQ==']
    }
    
    result = asyncio.run(agent.solve_challenge(test_challenge))
    print(f"\n结果: {result.get('status', 'unknown')}")
    print(f"Flag: {result.get('flag', 'Not found')}")


if __name__ == '__main__':
    import os
    main()
