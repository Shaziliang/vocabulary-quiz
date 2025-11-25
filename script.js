// 全局变量
let currentSession = null;
let currentQuestion = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadUnits();
});

// 加载单元列表
async function loadUnits() {
    try {
        const response = await fetch('/api/get_units');
        const units = await response.json();

        const unitButtons = document.getElementById('unit-buttons');
        unitButtons.innerHTML = '';

        for (const [unitName, questionCount] of Object.entries(units)) {
            const button = document.createElement('button');
            button.className = 'btn btn-primary btn-large';
            button.innerHTML = `${unitName}练习 (${questionCount}题)`;
            button.onclick = () => startUnitQuiz(unitName);
            unitButtons.appendChild(button);
        }
    } catch (error) {
        console.error('加载单元失败:', error);
        alert('加载单元列表失败，请刷新页面重试');
    }
}

// 开始单元练习
async function startUnitQuiz(unitName) {
    try {
        showLoading();
        const response = await fetch(`/api/start_unit/${encodeURIComponent(unitName)}`);
        const data = await response.json();

        currentSession = data.session_data;
        currentQuestion = data.question;

        showQuizScreen();
        displayQuestion();
    } catch (error) {
        console.error('开始练习失败:', error);
        alert('开始练习失败，请重试');
    } finally {
        hideLoading();
    }
}

// 开始乱序练习
async function startMixedQuiz() {
    try {
        showLoading();
        const response = await fetch('/api/start_mixed');
        const data = await response.json();

        currentSession = data.session_data;
        currentQuestion = data.question;

        showQuizScreen();
        displayQuestion();
    } catch (error) {
        console.error('开始乱序练习失败:', error);
        alert('开始练习失败，请重试');
    } finally {
        hideLoading();
    }
}

// 显示答题界面
function showQuizScreen() {
    hideAllScreens();
    document.getElementById('quiz-screen').classList.add('active');
}

// 显示题目
function displayQuestion() {
    if (!currentQuestion) return;

    // 更新进度信息
    document.getElementById('progress-text').textContent =
        `第 ${currentQuestion.question_number}/${currentQuestion.total_questions} 题`;
    document.getElementById('unit-name').textContent = currentQuestion.unit_name;
    document.getElementById('score').textContent = currentSession.score;

    // 显示原文
    document.getElementById('original-text').textContent = currentQuestion.original_text;

    // 显示选项
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';

    currentQuestion.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.className = 'option-btn';
        button.textContent = `${String.fromCharCode(65 + index)}. ${option}`;
        button.onclick = () => selectOption(button, option);
        optionsContainer.appendChild(button);
    });

    // 重置提交按钮
    document.getElementById('submit-btn').disabled = true;
}

// 选择选项
function selectOption(button, option) {
    // 移除其他选项的选中状态
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('selected');
    });

    // 设置当前选项为选中状态
    button.classList.add('selected');

    // 保存用户选择
    currentQuestion.userChoice = option;

    // 启用提交按钮
    document.getElementById('submit-btn').disabled = false;
}

// 提交答案
async function submitAnswer() {
    if (!currentQuestion.userChoice) {
        alert('请选择一个答案！');
        return;
    }

    try {
        showLoading();
        const response = await fetch('/api/check_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_data: currentSession,
                user_answer: currentQuestion.userChoice
            })
        });

        const data = await response.json();

        // 更新会话数据
        currentSession = data.session_data;

        // 显示结果
        showResultScreen(data.result);

        // 如果有下一题，预加载
        if (data.next_question) {
            currentQuestion = data.next_question;
        } else {
            currentQuestion = null;
        }

    } catch (error) {
        console.error('提交答案失败:', error);
        alert('提交答案失败，请重试');
    } finally {
        hideLoading();
    }
}

// 显示结果界面
function showResultScreen(result) {
    hideAllScreens();
    const resultScreen = document.getElementById('result-screen');
    resultScreen.classList.add('active');

    // 更新结果信息
    const icon = document.getElementById('result-icon');
    const title = document.getElementById('result-title');

    if (result.is_correct) {
        icon.textContent = '✅';
        title.textContent = '回答正确！';
        title.style.color = '#27ae60';
    } else {
        icon.textContent = '❌';
        title.textContent = '回答错误！';
        title.style.color = '#e74c3c';
    }

    // 显示答案详情
    document.getElementById('user-answer').textContent = result.user_answer;
    document.getElementById('correct-answer').textContent = result.correct_answer;
    document.getElementById('full-text').textContent = result.full_text;
    document.getElementById('translation-text').textContent = result.translation;

    // 更新下一题按钮状态
    const nextBtn = document.getElementById('next-btn');
    if (result.has_next) {
        nextBtn.style.display = 'block';
    } else {
        nextBtn.style.display = 'none';
    }
}

// 下一题
function nextQuestion() {
    if (currentQuestion) {
        showQuizScreen();
        displayQuestion();
    } else {
        showFinalResults();
    }
}

// 显示最终结果
function showFinalResults() {
    hideAllScreens();
    const finalScreen = document.getElementById('final-result-screen');
    finalScreen.classList.add('active');

    const accuracy = (currentSession.score / currentSession.total_answered * 100).toFixed(1);

    // 更新统计信息
    document.getElementById('final-unit').textContent = currentSession.unit_name;
    document.getElementById('final-total').textContent = currentSession.total_answered;
    document.getElementById('final-correct').textContent = currentSession.score;
    document.getElementById('final-accuracy').textContent = `${accuracy}%`;

    // 显示评价
    const comment = document.getElementById('final-comment');
    if (accuracy >= 90) {
        comment.textContent = '🎉 优秀！继续保持！';
        comment.style.color = '#27ae60';
    } else if (accuracy >= 70) {
        comment.textContent = '👍 良好！继续努力！';
        comment.style.color = '#f39c12';
    } else if (accuracy >= 60) {
        comment.textContent = '💪 及格！多加练习！';
        comment.style.color = '#e67e22';
    } else {
        comment.textContent = '📚 需要更多练习！';
        comment.style.color = '#e74c3c';
    }
}

// 重新开始练习
function restartQuiz() {
    if (currentSession.unit_name === '所有单元混合') {
        startMixedQuiz();
    } else {
        startUnitQuiz(currentSession.unit_name);
    }
}

// 显示统计
function showStatistics() {
    hideAllScreens();
    const statsScreen = document.getElementById('stats-screen');
    statsScreen.classList.add('active');

    const statsContent = document.getElementById('stats-content');

    if (!currentSession || currentSession.total_answered === 0) {
        statsContent.innerHTML = '<p>尚未完成任何题目</p>';
    } else {
        const accuracy = (currentSession.score / currentSession.total_answered * 100).toFixed(1);
        statsContent.innerHTML = `
            <div class="stats-grid">
                <div class="stat-item">
                    <label>总答题数:</label>
                    <span>${currentSession.total_answered}</span>
                </div>
                <div class="stat-item">
                    <label>正确题数:</label>
                    <span>${currentSession.score}</span>
                </div>
                <div class="stat-item">
                    <label>准确率:</label>
                    <span>${accuracy}%</span>
                </div>
            </div>
        `;
    }
}

// 返回主菜单
function backToMenu() {
    hideAllScreens();
    document.getElementById('main-menu').classList.add('active');
}

// 工具函数
function hideAllScreens() {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
}

function showLoading() {
    // 可以在这里添加加载指示器
    document.body.style.cursor = 'wait';
}

function hideLoading() {
    document.body.style.cursor = 'default';
}

// 添加键盘快捷键支持
document.addEventListener('keydown', function(event) {
    // 数字键 1-4 选择选项
    if (event.key >= '1' && event.key <= '4' && document.getElementById('quiz-screen').classList.contains('active')) {
        const index = parseInt(event.key) - 1;
        const options = document.querySelectorAll('.option-btn');
        if (options[index]) {
            options[index].click();
        }
    }

    // Enter 键提交答案
    if (event.key === 'Enter' && document.getElementById('quiz-screen').classList.contains('active')) {
        const submitBtn = document.getElementById('submit-btn');
        if (!submitBtn.disabled) {
            submitBtn.click();
        }
    }

    // 空格键下一题
    if (event.key === ' ' && document.getElementById('result-screen').classList.contains('active')) {
        const nextBtn = document.getElementById('next-btn');
        if (nextBtn.style.display !== 'none') {
            nextBtn.click();
        }
    }
});