from flask import Flask, render_template, jsonify, request
import random
import os
import json

app = Flask(__name__)

# 题库数据（与原始代码相同）
question_bank = {
    "Unit 1": [
        {
            "keyword": "detrimental",
            "original_text": "Given the detrimental effect of smoking on health, Healthy People 2010 seeks to reduce the prevalence of smoking from 24% in 1998 to ≤12% by 2010.",
            "translation": "鉴于吸烟对健康的有害影响，《2010年健康人群》计划将1998年的24%吸烟率到2010年降至≤12%。",
            "distractors": ["harmful", "damaging", "adverse"]
        },
        {
            "keyword": "depression",
            "original_text": "How many days was your mental health, which includes stress, depression, and problems with emotions, not good?",
            "translation": "你有多少天的心理健康状况不佳，包括压力、抑郁和情绪问题？",
            "distractors": ["despondency", "melancholy", "gloom"]
        },
        {
            "keyword": "symptom",
            "original_text": "How many days did you feel sad, blue or depressed? (depressive symptoms).",
            "translation": "你感受到悲伤、抑郁或沮丧多少天了？（抑郁症状）",
            "distractors": ["indication", "manifestation", "sign"]
        },
        {
            "keyword": "measure",
            "original_text": "These measures are of moderate to high reliability and validity.",
            "translation": "这些指标具有中等到高的信度和效度。",
            "distractors": ["metric", "indicator", "parameter"]
        },
        {
            "keyword": "intervention",
            "original_text": "In short, smoking may represent the 'tip of the iceberg' of a number of modifiable risk factors meriting intervention.",
            "translation": "简而言之，吸烟可能代表了许多值得干预的可改变风险因素的'冰山一角'。",
            "distractors": ["interference", "mediation", "involvement"]
        },
        {
            "keyword": "cessation",
            "original_text": "It is well known that smoking is frequently associated with alcohol consumption, and that smoking cessation is often associated with weight gain.",
            "translation": "众所周知，吸烟通常与饮酒有关，而戒烟通常与体重增加有关。",
            "distractors": ["termination", "discontinuation", "stoppage"]
        },
        {
            "keyword": "implication",
            "original_text": "Notably, smoking poses serious economic implications as well, accounting for >$75 billion per year in medical costs and $82 billion per year in lost productivity.",
            "translation": "值得注意的是，吸烟也会带来严重的经济影响，每年会造成超过750亿美元的医疗费用和820亿美元的生产力损失。",
            "distractors": ["consequence", "ramification", "repercussion"]
        },
        {
            "keyword": "productivity",
            "original_text": "Notably, smoking poses serious economic implications as well, accounting for >$75 billion per year in medical costs and $82 billion per year in lost productivity.",
            "translation": "值得注意的是，吸烟也会带来严重的经济影响，每年造成超过750亿美元的医疗费用和820亿美元的生产力损失。",
            "distractors": ["efficiency", "output", "yield"]
        },
        {
            "keyword": "reference",
            "original_text": "The remaining eight questions were about self-assessed health referenced to the past 30 days.",
            "translation": "其余的8个问题是关于过去30天的自我评估健康状况。",
            "distractors": ["relation", "connection", "correlation"]
        },
        {
            "keyword": "distress",
            "original_text": "As Table 2 indicates, after adjusting for socio-demographic characteristics, those who currently smoked were significantly more likely than those who never smoked to have impairments in all of the HRQOL measures examined (fair/poor general health, infrequent vitality, and frequent episodes of physical distress, mental distress, depressive symptoms, anxiety symptoms, pain, sleep impairment, and activity limitation).",
            "translation": "如表2所示，在对社会人口学特征进行调整之后，最近吸烟的人比从未吸烟的人更有可能在所有健康相关生活质量的检测指标（总体健康状况良好/差，缺乏活力，经常出现身体上和精神上的不适、抑郁症状、焦虑症状、疼痛、睡眠障碍和活动受限）方面出现损伤。",
            "distractors": ["suffering", "anguish", "torment"]
        },
        {
            "keyword": "depress",
            "original_text": "How many days did you feel sad, blue or depressed? (depressive symptoms)",
            "translation": "你有多少天感到悲伤抑郁或抑郁？（抑郁症状）",
            "distractors": ["sadden", "dishearten", "discourage"]
        },
        {
            "keyword": "a constellation of",
            "original_text": "Thus, smoking appears to be associated with a constellation of health behaviors, potentially further compounding its adverse effects.",
            "translation": "因此，吸烟似乎与一系列健康行为有关，可能进一步加剧其不利影响。",
            "distractors": ["a cluster of", "a group of", "a set of"]
        },
        {
            "keyword": "an array of",
            "original_text": "Thus, smoking appears to be associated with an array of health behaviors, potentially further compounding its adverse effects.",
            "translation": "因此，吸烟似乎与一系列健康行为有关，可能进一步加剧其不利影响。",
            "distractors": ["a variety of", "a range of", "a selection of"]
        },
        {
            "keyword": "vitality",
            "original_text": "'How many days did you feel very healthy and full of energy?'(vitality)",
            "translation": "活力充沛",
            "distractors": ["energy", "vigor", "liveliness"]
        },
        {
            "keyword": "recreation",
            "original_text": "'How many days did poor physical or mental health keep you from doing your usual activities, such as self-care, work, or recreation?'",
            "translation": "不好的身体或精神健康让你多久无法从事你的诸如自我照顾、工作或娱乐这种日常活动了？",
            "distractors": ["leisure", "amusement", "entertainment"]
        },
        {
            "keyword": "dichotomize",
            "original_text": "Responses were dichotomized into <14(infrequent) and >=14(frequent) unhealthy days in each domain.",
            "translation": "在每个域中，应答被分为<14(不常见)>=（常见）不健康天数",
            "distractors": ["divide", "split", "separate"]
        },
        {
            "keyword": "intake",
            "original_text": "The BRFSS also included questions about leisure-time physical activity, height and weight, alcohol consumption, and fruit and vegetable intake.",
            "translation": "BRFSS还包括关于休闲时间体育活动、体重和体重、饮酒以及水果和蔬菜摄入量的问题。",
            "distractors": ["consumption", "ingestion", "absorption"]
        },
        {
            "keyword": "moderate",
            "original_text": "These measures are of moderate to high reliability and validity.",
            "translation": "这些指标是从温和的到高值度和效度的。",
            "distractors": ["medium", "average", "reasonable"]
        },
        {
            "keyword": "episode",
            "original_text": "As Table 2 indicates, after adjusting for socio-demographic characteristics, those who currently smoked were significantly more likely than those who never smoked to have impairments in all of the HRQOL measures examined (fair/poor general health, infrequent vitality, and frequent episodes of physical distress, mental distress, depressive symptoms, anxiety symptoms, pain, sleep impairment, and activity limitation).",
            "translation": "如表2所示，在调整社会人口特征后，目前吸烟的人比从未吸烟的人更有可能在所检查的所有HRQOL措施（一般健康一般不佳、活力不频繁、经常出现身体不适、精神困扰、抑郁症状、焦虑症状、疼痛、睡眠障碍和活动限制）中出现损害。",
            "distractors": ["occurrence", "incident", "event"]
        },
        {
            "keyword": "obese",
            "original_text": "Respondents who currently smoke were more likely than former smokers or never smokers to be heavy or binge drinkers, but were less likely to be obese.",
            "translation": "目前吸烟的受访者比以前吸烟或从不吸烟的人更有可能酗酒或酗酒，但肥胖的可能性较小。",
            "distractors": ["overweight", "corpulent", "fat"]
        },
        {
            "keyword": "initiation",
            "original_text": "Research suggests that fears about weight gain may motivate the initiation or continuation of smoking, especially among women.",
            "translation": "研究表明，对体重增加的恐惧可能会促使人们开始或继续吸烟，特别是在女性中。",
            "distractors": ["start", "commencement", "beginning"]
        },
        {
            "keyword": "continuation",
            "original_text": "Research suggests that fears about weight gain may motivate the initiation or continuation of smoking, especially among women.",
            "translation": "研究表明，对体重增加的恐惧可能促使人们开始或继续吸烟。",
            "distractors": ["continuance", "persistence", "prolongation"]
        },
        {
            "keyword": "merit",
            "original_text": "In short, smoking may represent the 'tip of the iceberg' of a number of modifiable risk factors meriting intervention.",
            "translation": "简而言之，吸烟可能代表了许多值得干预的可改变风险因素的'冰山一角'。",
            "distractors": ["deserve", "earn", "warrant"]
        },
        {
            "keyword": "reside",
            "original_text": "These results suggest that there is a significant association between smoking and impaired mental health among both men and women residing in the community.",
            "translation": "这些结果表明，在社区居住的男性和女性中，吸烟与精神健康受损之间存在显著的关联。",
            "distractors": ["live", "dwell", "inhabit"]
        },
        {
            "keyword": "bias",
            "original_text": "Third, these analyses are based on self-reported data, and therefore these results could be influenced by reporting biases.",
            "translation": "第三，这些分析是基于自我报告的数据，因此这些结果可能会受到报告偏差的影响。",
            "distractors": ["prejudice", "partiality", "inclination"]
        },
        {
            "keyword": "representative",
            "original_text": "Fourth, because the analysis was based on date from 23 states and District of Columbia, the results may, conceivably, not be representative of the entire United States.",
            "translation": "第四，由于分析是基于23个州和哥伦比亚特区的数据，因此可以想象，结果可能无法代表整个美国。",
            "distractors": ["typical", "characteristic", "exemplary"]
        },
        {
            "keyword": "motivate",
            "original_text": "Research suggests that fears about weight gain may motivate the initiation or continuation of smoking, especially among women.",
            "translation": "研究表明，对体重增加的恐惧可能会促使人们开始或继续吸烟，特别是在女性中。",
            "distractors": ["inspire", "stimulate", "prompt"]
        },
        {
            "keyword": "impair",
            "original_text": "Compared to former smokers, adjusted analyses revealed that current smokers were significantly more likely to have impaired HROOL on seven of the nine HROOL measures.",
            "translation": "与以前的吸烟者相比，调整后的分析显示，目前的吸烟者在几项健康相关生活质量指标中的七项上更有可能达到健康相关生活质量。",
            "distractors": ["weaken", "diminish", "damage"]
        },
        {
            "keyword": "conceivably",
            "original_text": "the results may, conceivably, not be representative of the entire United States.",
            "translation": "可以想象的是，这些结果可能不能代表整个美国。",
            "distractors": ["possibly", "plausibly", "imaginably"]
        },
        {
            "keyword": "infer",
            "original_text": "Second, because the study was cross-sectional, causality cannot be inferred.",
            "translation": "其次，由于研究是横断面的，因此无法推断因果关系。",
            "distractors": ["deduce", "conclude", "derive"]
        },
        {
            "keyword": "prevalence",
            "original_text": "with the exception of those aged 35 to 44 years as age increased, the prevalence of current smoking decreased,",
            "translation": "除了35到44岁的人之外，随着年龄的增长，当前吸烟的流行率下降。",
            "distractors": ["frequency", "commonness", "ubiquity"]
        },
        {
            "keyword": "stress",
            "original_text": "How many days was your mental health, which includes stress, depression, and problems with emotions, not good?",
            "translation": "你有多少天的心理健康状况不佳，包括压力、抑郁和情绪问题？",
            "distractors": ["pressure", "tension", "strain"]
        },
        {
            "keyword": "pose",
            "original_text": "Notably, smoking poses serious economic implications as well, accounting for ≥ 575 billion per year in medical costs and $82 billion per year in lost productivity.",
            "translation": "值得注意的是，吸烟也造成了严重的经济影响，每年造成超过750亿美元的医疗费用和820亿美元的生产力损失。",
            "distractors": ["present", "create", "constitute"]
        },
        {
            "keyword": "total",
            "original_text": "Finally, the number of fruits and vegetables eaten per day were totaled to determine whether the respondent was consuming at the least recommended minimum of five servings.",
            "translation": "最后，将每天吃的水果和蔬菜的数量加起来，以确定受访者是否摄入了至少推荐的五份。",
            "distractors": ["sum", "aggregate", "accumulate"]
        },
        {
            "keyword": "physical inactivity",
            "original_text": "As physical inactivity, inadequate sleep, and low consumption of fruits and vegetables have each been associated with increased morbidity and mortality...",
            "translation": "缺乏运动，睡眠不足，以及少吃水果和蔬菜都会增加发病率和死亡率...",
            "distractors": ["sedentary lifestyle", "lack of exercise", "inactivity"]
        },
        {
            "keyword": "inadequate sleep",
            "original_text": "As physical inactivity, inadequate sleep, and low consumption of fruits and vegetables have each been associated with increased morbidity and mortality...",
            "translation": "缺乏运动，睡眠不足，以及少吃水果和蔬菜都会增加发病率和死亡率...",
            "distractors": ["insufficient sleep", "poor sleep", "sleep deprivation"]
        },
        {
            "keyword": "morbidity",
            "original_text": "As physical inactivity, inadequate sleep, and low consumption of fruits and vegetables have each been associated with increased morbidity and mortality...",
            "translation": "缺乏运动，睡眠不足，以及少吃水果和蔬菜都会增加发病率和死亡率...",
            "distractors": ["illness", "disease", "sickness"]
        },
        {
            "keyword": "mortality",
            "original_text": "As physical inactivity, inadequate sleep, and low consumption of fruits and vegetables have each been associated with increased morbidity and mortality...",
            "translation": "缺乏运动，睡眠不足，以及少吃水果和蔬菜都会增加发病率和死亡率...",
            "distractors": ["death", "fatality", "loss"]
        },
        {
            "keyword": "physician",
            "original_text": "...the presence of smoking should alert the physician to the possible coexistence of other adverse health behaviors...",
            "translation": "...吸烟的存在应按照医生注意可能同时存在的其他不良健康行为...",
            "distractors": ["doctor", "medical practitioner", "clinician"]
        },
        {
            "keyword": "coexistence",
            "original_text": "...the presence of smoking should alert the physician to the possible coexistence of other adverse health behaviors...",
            "translation": "...吸烟的存在应按照医生注意可能同时存在的其他不良健康行为...",
            "distractors": ["simultaneous existence", "concurrence", "co-occurrence"]
        },
        {
            "keyword": "compound",
            "original_text": "...that may compound its deleterious consequences.",
            "translation": "...这些行为可能会加重其有害后果。",
            "distractors": ["worsen", "intensify", "aggravate"]
        },
        {
            "keyword": "deleterious",
            "original_text": "...that may compound its deleterious consequences.",
            "translation": "...这些行为可能会加重其有害后果。",
            "distractors": ["harmful", "damaging", "detrimental"]
        }
    ],
    "Unit 2": [
        {
            "keyword": "interactive",
            "original_text": "The main research question is, 'How does students' understanding of the greenhouse effect and global warming change after participating in a technology-enhanced learning environment featuring virtual experiments with an interactive visualization?'",
            "translation": "主要的研究问题是:'在参与以交互式可视化的虚拟实验为特色的技术增强学习环境后，学生对温室效应和全球变暖变化的理解如何?'",
            "distractors": ["participatory", "responsive", "engaging"]
        },
        {
            "keyword": "module",
            "original_text": "We measure students' representations by analyzing their responses to a series of open-ended questions about the concepts covered in the module.",
            "translation": "我们通过分析学生们对一系列开放式问题的回答来衡量他们的理解程度，这些问题涉及到模块中所涵盖的概念。",
            "distractors": ["unit", "component", "segment"]
        },
        {
            "keyword": "visualization",
            "original_text": "The main research question is, 'How does students' understanding of the greenhouse effect and global warming change after participating in a technology-enhanced learning environment featuring virtual experiments with an interactive visualization?'",
            "translation": "在参与以交互式可视化虚拟实验为特色的虚拟增强学习环境后，学生对温室效应和全球变暖变化的理解如何？",
            "distractors": ["representation", "display", "illustration"]
        },
        {
            "keyword": "framework",
            "original_text": "A group of researchers familiar with the curriculum unit design and the knowledge integration framework reviewed the rubric and the example responses to ensure that the correct criteria would be applied to the data.",
            "translation": "一组熟悉课程单元设计和知识整合框架的研究人员审查了评估标准和示例回复，以确保正确的标准应用于数据。",
            "distractors": ["structure", "schema", "architecture"]
        },
        {
            "keyword": "pre-service",
            "original_text": "Other work shows that some pre-service teachers also attribute the cause of climate change to the depletion of the ozone layer (Papadimitriou, 2004).",
            "translation": "其他研究表明，一些职前教师也将气候变化的原因归因于臭氧层的损耗",
            "distractors": ["trainee", "prospective", "candidate"]
        },
        {
            "keyword": "depletion",
            "original_text": "Other work shows that some pre-service teachers also attribute the cause of climate change to the depletion of the ozone layer.",
            "translation": "其他研究表明，一些岗前老师也将气候变化的原因归因于臭氧层的损耗。",
            "distractors": ["exhaustion", "reduction", "diminution"]
        },
        {
            "keyword": "target",
            "original_text": "In this study, in order for students to receive credit as having an integrated understanding of a target concept or phenomenon, their responses must have correct, interconnected ideas.",
            "translation": "在这项研究中，为了让学生获得对目标概念或现象有完整理解的学分，他们的回答必须有正确的、相关互联的想法",
            "distractors": ["objective", "goal", "aim"]
        },
        {
            "keyword": "representation",
            "original_text": "They found that these students had several different representations of the greenhouse effect",
            "translation": "他们发现这些学生对温室效应有几种不同的表述",
            "distractors": ["depiction", "portrayal", "rendering"]
        },
        {
            "keyword": "misconception",
            "original_text": "Data from Meadows and Wiesenmayer's (1999) study indicate that some students have incorporated this misconception into their knowledge frameworks of global warming and use it to reason about all issues related to the global warming phenomenon.",
            "translation": "Meadows和Wiesenmayer (1999) 的研究数据表明的情况，使一些学生将这种误解纳入了他们对全球变暖的已知框架中，并用它来推理与全球变暖现象相关的大部分问题。",
            "distractors": ["misunderstanding", "fallacy", "delusion"]
        },
        {
            "keyword": "prompt",
            "original_text": "Throughout these experimentation reflection steps, embedded notes prompt students to generate hypotheses, gather evidence, draw conclusions, and make connections between new and pre-existing ideas.",
            "translation": "在这些实验反思步骤中，嵌入式笔记促使学生提出假设，收集证据，得出结论，并在新想法和现有想法之间建立联系。",
            "distractors": ["encourage", "urge", "stimulate"]
        },
        {
            "keyword": "embed",
            "original_text": "Throughout these experimentation reflection steps, embedded notes prompt students to generate hypotheses, gather evidence, draw conclusions, and make connections between new and pre-existing ideas.",
            "translation": "在这些实验反思步骤中，嵌入式笔记促使学生提出假设，收集证据，得出结论，并在新想法和现有想法之间建立联系。",
            "distractors": ["insert", "incorporate", "integrate"]
        },
        {
            "keyword": "integrate",
            "original_text": "Following participation in the GWVE unit activities, students' ideas were more normative and better integrated.",
            "translation": "参加完GWVE单元活动后，学生的想法更加规范，更加完整。",
            "distractors": ["combine", "unify", "incorporate"]
        },
        {
            "keyword": "numerical",
            "original_text": "The results of their manipulation will show a numerical representation of the concentration of greenhouse gases in the atmosphere, the temperature of the Earth and the albedo level.",
            "translation": "他们对模型的操作结果将显示出大气中温室气体浓度、地球温度和反照率水平的数值表示。",
            "distractors": ["digital", "quantitative", "mathematical"]
        },
        {
            "keyword": "fluctuation",
            "original_text": "Additionally, there is a graph representing the temperature fluctuations that occur as a result of students' manipulations (Tinker, 2005).",
            "translation": "此外，还有一张图表，表示因学生操纵而发生的温度波动(Tinker, 2005年)。",
            "distractors": ["variation", "oscillation", "change"]
        },
        {
            "keyword": "enact",
            "original_text": "Five teachers from three schools on the west coast and two schools in the southeastern US enacted the curriculum unit in their sixth grade science classes.",
            "translation": "来自西海岸3所学校和美国东南部2所学校的5名教师在他们的6年级科学课堂上实施了这些课程单元。",
            "distractors": ["implement", "execute", "perform"]
        },
        {
            "keyword": "normative",
            "original_text": "Following participation in the GWVE unit activities, students' ideas were more normative and better integrated.",
            "translation": "参加完GWVE单元活动后，学生的想法更加规范，更加完整。",
            "distractors": ["standard", "conventional", "typical"]
        },
        {
            "keyword": "sum",
            "original_text": "Scores from each question were summed to calculate an overall learning score.",
            "translation": "对每个问题的分数进行累加，以计算总体学习得分。",
            "distractors": ["total", "aggregate", "accumulate"]
        },
        {
            "keyword": "trap",
            "original_text": "I think the greenhouse effect happens when solar energy is trapped in the stratosphere.",
            "translation": "例如，一名学生写道：'我认为温室效应是当太阳能被困在平流层时发生的。'",
            "distractors": ["catch", "ensnare", "capture"]
        },
        {
            "keyword": "reliability",
            "original_text": "Twenty percent of the tests were code by a second researcher for reliability (97%)",
            "translation": "百分之二十的测试由第二位研究人员编码，以保证可靠性(97%)",
            "distractors": ["dependability", "consistency", "trustworthiness"]
        },
        {
            "keyword": "credit",
            "original_text": "In this study, in order for students to receive credit as having an integrated understanding of a target concept or phenomenon, their responses must have correct, interconnected ideas.",
            "translation": "在这项研究中，为了让学生获得对目标概念或现象有综合理解的学分，他们的回答必须有正确的、互相关联的想法。",
            "distractors": ["recognition", "acknowledgment", "merit"]
        },
        {
            "keyword": "interconnect",
            "original_text": "In this study, in order for students to receive credit as having an integrated understanding of a target concept or phenomenon, their responses must have correct, interconnected ideas.",
            "translation": "在这项研究中，为了让学生获得对目标概念或现象有综合理解的学分，他们的回答必须有正确的、相互关联的想法。",
            "distractors": ["link", "network", "interweave"]
        },
        {
            "keyword": "incremental",
            "original_text": "Knowledge accounts for incremental changes by identifying levels of understanding based on ideas and links between ideas.",
            "translation": "知识通过识别基于想法和想法之间的联系的理解水平来说明增量变化。",
            "distractors": ["gradual", "step-by-step", "progressive"]
        },
        {
            "keyword": "intermediate",
            "original_text": "In their work on children's knowledge of the Earth, Vosniadou and Brewer identify intermediate mental models that represent children's attempts to reconcile new knowledge that the Earth is a sphere with their preexisting knowledge that the earth is flat.",
            "translation": "在他们关于儿童对地球知识的研究中，Vosniadou和Brewer确定了中间心理模型，这些模型代表了儿童试图调和地球是一个球体的新知识与他们先前存在的地球是平的知识",
            "distractors": ["middle", "transitional", "intervening"]
        }
    ],
    "Unit 3": [
        {
            "keyword": "underscore",
            "original_text": "In 1983, the World Health Organization called attention to the world-wide decline in the prevalence and duration of breast-feeding, and underscored the urgent need for more definitive data on present-day infant-feeding practices and trends, as well as information on the key factors influencing women's decisions on how to feed their babies.",
            "translation": "1983年，世界卫生组织呼吁注意全世界母乳喂养的普遍性和持续时间下降，并强调迫切需要更确切的数据，以了解当今婴儿喂养的做法和趋势，以及影响妇女决定如何喂养婴儿的关键因素。",
            "distractors": ["emphasize", "highlight", "stress"]
        },
        {
            "keyword": "duration",
            "original_text": "In 1983, the World Health Organization called attention to the world-wide decline in the prevalence and duration of breast-feeding, and underscored the urgent need for more definitive data on present-day infant-feeding practices and trends, as well as information on the key factors influencing women's decisions on how to feed their babies.",
            "translation": "1983年，世界卫生组织呼吁注意全世界母乳喂养普遍性以及持续时间减少的问题，并强调需要更准确的数据来了解目前婴儿喂养的方式和趋势，以及影响母亲喂养孩子方式的关键因素是什么。",
            "distractors": ["period", "length", "span"]
        },
        {
            "keyword": "erroneous",
            "original_text": "The dimensions of this rapid, pervasive socio-cultural transformation, often erroneously regarded as a symbol of modernity, as well as the forces underlying the disturbing negative change, are not yet clearly defined.",
            "translation": "这种迅速而普遍的社会文化变革往往被错误地视为现代化的象征，而这种令人不安的消极变化背后的力量尚未得到明确界定。",
            "distractors": ["mistaken", "incorrect", "inaccurate"]
        },
        {
            "keyword": "prolong",
            "original_text": "It is clear that such explanations are oversimplified and apply to only a few and ignore the hard realities of urban existence that may make prolonged breast-feeding difficult.",
            "translation": "显然，这种解释过于简单化，仅适用于少数情况，而且忽略了城市生活的严峻现实，这些现实可能会使长期母乳喂养变得困难。",
            "distractors": ["extend", "lengthen", "continue"]
        },
        {
            "keyword": "illiterate",
            "original_text": "Quite often the actual practice fell short of the mother's nutritional awareness, thus contradicting the frequently repeated statements that such illiterate, urbanized women are victims of poor or improper counseling.",
            "translation": "很常见的是，实际的做法未能达到母亲的营养认知，因此与那些反复提到的说法相矛盾，也就是说这些文盲的城市女性是缺乏或不当咨询的受害者。",
            "distractors": ["uneducated", "unschooled", "unlettered"]
        },
        {
            "keyword": "maternal",
            "original_text": "This report attempts to evaluate current maternal perceptions of infant-feeding among different ethnic, religious, cultural, and socio-economic groups in Nigeria, with the primary objective of assessing the extent of decline in breast-feeding as well as the major factors responsible for the negative change, and how best to institute corrective educational measures.",
            "translation": "本报告试图评估尼日利亚不同种族、宗教、文化和社会经济群体中当前母亲对婴儿喂养的看法，主要目的是评估母乳喂养减少的程度，造成这种负面变化的主要因素，以及如何最好地制定纠正性教育措施。",
            "distractors": ["motherly", "parental", "mother"]
        },
        {
            "keyword": "supplement",
            "original_text": "Only 4 percent of the mothers believed that breast feeding should be supplemented for infants under one month of age.",
            "translation": "只有4%的母亲认为一个月以下的婴儿应补充母乳喂养。",
            "distractors": ["complement", "augment", "add"]
        },
        {
            "keyword": "prestige",
            "original_text": "There is good evidence from the present study that breast-feeding has not lost its prestige among the economically underprivileged laboring classes in metropolitan Lagos.",
            "translation": "本研究有充分证据表明，母乳喂养在Lagos大城市经济贫困的劳动阶层中并没有失去声望",
            "distractors": ["status", "reputation", "esteem"]
        },
        {
            "keyword": "migrate",
            "original_text": "The crucial questions, as rightly pointed out by Harfouche (1980), are why and how 'women who migrate from the traditional rural areas to the so-called modern universe adjust to new situations, adopt new attitudes and patterns of behavior.'",
            "translation": "关键的问题，正如哈福什正确指出的那样（1980），是为什么和如何从传统农村地区迁移的妇女到所谓的现代世界适应新的情况，采取新的态度和行为模式。",
            "distractors": ["relocate", "move", "resettle"]
        },
        {
            "keyword": "implicit",
            "original_text": "Implicit in this is a great pressure on mothers to spend more time trying to augment the family income at the expense of caring adequately for their children.",
            "translation": "这隐含着对母亲的巨大压力，要求她们花更多时间努力增加家庭收入，而牺牲对孩子的充分照顾。",
            "distractors": ["implied", "suggested", "understood"]
        },
        {
            "keyword": "counseling",
            "original_text": "Quite often the actual practice fell short of the mother's nutritional awareness, thus contradicting the frequently repeated statements that such illiterate, urbanized women are victims of poor or improper counseling.",
            "translation": "实际上，这些文盲妇女的营养意识往往高于她们的实际饮食习惯，这与人们经常重复的说法相矛盾，即这些没有文化的、城市化的妇女是缺乏或不当咨询的受害者。",
            "distractors": ["advice", "guidance", "consultation"]
        },
        {
            "keyword": "metropolitan",
            "original_text": "There is good evidence from the present study that breast-feeding has not lost its prestige among the economically underprivileged laboring classes in metropolitan Lagos, but is accorded lower priority because of the overwhelming competing factors of urban existence resulting from poverty.",
            "translation": "本研究有充分的证据表明，母乳喂养在Lagos大都市的贫困劳工阶层中并未失去其地位，但由于贫困导致的都市生活因素的巨大竞争压力，导致母乳喂养被置于次要地位。",
            "distractors": ["urban", "city", "cosmopolitan"]
        },
        {
            "keyword": "corrective",
            "original_text": "This report attempts to evaluate current maternal perceptions of infant-feeding among different ethnic, religious, cultural, and socio-economic groups in Nigeria, with the primary objective of assessing the extent of decline in breast-feeding as well as the major factors responsible for the negative change, and how best to institute corrective educational measures.",
            "translation": "本报告试图评估尼日利亚不同种族、宗教、文化和社会经济群体中当前母亲对婴儿喂养的看法，主要目的是评估母乳喂养减少的程度、造成这种负面变化的主要因素，以及如何更好地制定纠正性教育措施。",
            "distractors": ["remedial", "rectifying", "amendatory"]
        },
        {
            "keyword": "subsistence",
            "original_text": "No fewer than 29% of the families had monthly incomes below N 200, well below the subsistence level in a city rated among the most expensive in the world in terms of housing and general cost of living.",
            "translation": "不少于29%的家庭月收入低于200纳克法郎，在这个住房和一般生活费用被评为世界上最昂贵的城市里，这远远低于维持生计的水平。",
            "distractors": ["survival", "livelihood", "sustenance"]
        },
        {
            "keyword": "hygienically",
            "original_text": "Perhaps more lasting benefits will be achieved by emphasizing the education of mothers on how to prepare and use hygienically acceptable supplementary foods from relatively inexpensive but nutritious locally available staple foods.",
            "translation": "也许通过强调教育母亲如何用当地相对便宜但营养丰富的主食制作和使用卫生上可接受的辅食，将会获得更持久的好处。",
            "distractors": ["sanitarily", "cleanly", "sterilely"]
        },
        {
            "keyword": "composition",
            "original_text": "For this particular study, Surulere, a suburb of metropolitan Lagos that is heterogeneous in its ethnic and socio-economic composition, was selected as a pretest area for the widely assumed negative effects of urbanization and modernization on infant-feeding practices and traditional African image of mothering.",
            "translation": "对于这项特别的研究，大都市拉各斯的一个郊区，在种族和社会经济构成上是异质性的，被选为预测城区，以广泛假设的城市化和现代化对婴儿喂养实践和传统非洲母亲形象的负面影响。",
            "distractors": ["makeup", "constitution", "formation"]
        },
        {
            "keyword": "reverse",
            "original_text": "Until this major structural defect of urban life in the developing world is eliminated or controlled, any nutrition education program that solely emphasizes and extols the virtues of breast-feeding, facts already well accepted by the people, is bound to achieve minimal results in terms of reversing the current trend towards increasing displacement of breast-feeding by bottle-feeding.",
            "translation": "在消除或控制发展中国家城市生活的这一重大结构缺陷之前，任何只强调和赞扬母乳喂养美德的营养教育计划，这些事实已经被人们广泛接受，在扭转目前通过奶瓶喂养取代母乳喂养的趋势方面必然会取得最低限度的成果。",
            "distractors": ["overturn", "invert", "counteract"]
        },
        {
            "keyword": "impoverished",
            "original_text": "Too much educational effort has been spent on trying to teach impoverished, urbanized women precisely when to introduce supplementary feeding, when it is often forgotten that even among nutrition experts there is still lack of unanimity on this issue (Scrimshaw and Underwood,1980;Scrimshaw,1982).",
            "translation": "人们花费了太多的教育精力来尝试教导贫困、城市化的妇女何时引入补充喂养，而人们往往忘记了，",
            "distractors": ["poor", "destitute", "needy"]
        },
        {
            "keyword": "unanimity",
            "original_text": "Too much educational effort has been spent on trying to teach impoverished, urbanized women precisely when to introduce supplementary feeding, when it is often forgotten that even among nutrition experts there is still lack of unanimity on this issue (Scrimshaw and Underwood, 1980; Scrimshaw, 1982).",
            "translation": "即使在营养专家之间，在这个问题上仍然缺乏共识。",
            "distractors": ["agreement", "consensus", "harmony"]
        },
        {
            "keyword": "entertain",
            "original_text": "Our data demonstrated quite convincingly that virtually all the mothers, most of whom had little or no formal education studied, still entertained strong positive feelings about the importance of breast-feeding, an observation consistent with the reported findings of Goyca and Johnson (Goyca and Johnson, 1977).",
            "translation": "我们的数据相当令人信服地表明，几乎所有的母亲，其中大多数人很少或没有接受过正规教育，仍然对母乳喂养的重要性抱有强烈的积极情绪。这一观察结果与Goyca和Johnson (Goyca和Johnson,1977)的报告结果一致。",
            "distractors": ["hold", "harbor", "cherish"]
        },
        {
            "keyword": "pervasive",
            "original_text": "The dimensions of this rapid, pervasive socio-cultural transformation, often erroneously regarded as a symbol of modernity, as well as the forces underlying the disturbing negative change, are not yet clearly defined.",
            "translation": "这种迅速、普遍的社会文化变革往往被错误地视为现代性的象征，其规模以及令人不安的情报变化背后的力量尚未明确界定。",
            "distractors": ["widespread", "permeating", "ubiquitous"]
        },
        {
            "keyword": "augment",
            "original_text": "Implicit in this is a great pressure on mothers to spend more time trying to augment the family income at the expense of caring adequately for their children.",
            "translation": "这隐含着对母亲的巨大压力，她们要花更多时间试图以牺牲照顾为代价来增加家庭收入",
            "distractors": ["increase", "enhance", "boost"]
        },
        {
            "keyword": "augmentation",
            "original_text": "Implicit in this is a great pressure on mothers to spend more time trying to augment the family income at the expense of caring adequately for their children.",
            "translation": "这隐含着对母亲的巨大压力，她们要花更多时间试图以牺牲照顾为代价来增加家庭收入",
            "distractors": ["increase", "enhancement", "boost"]
        }
    ],
    "Unit 4": [
        {
            "keyword": "inherent",
            "original_text": "Four main sources of the hazards of GMO are discussed by scientists worldwide:1) those due to the new genes, and gene products introduced;2) unintended effects inherent to the technology;",
            "translation": "全球科学家讨论了转基因生物（GMO）危害的四个主要来源：1)由于引入的新基因和基因产物所导致的；2)技术本身固有的非预期效应；",
            "distractors": ["intrinsic", "innate", "natural"]
        },
        {
            "keyword": "organism",
            "original_text": "The term genetically modified organism (GMOs) refers to plants, microbes and animals with genes transferred from other species in order to produce certain novel characteristics (for example resistances, or herbicides) and are produced by recombinant DNA technology.",
            "translation": "转基因生物（GMO）一词是指具有从其他物种转移的基因的植物、微生物和动物，以产生某些新的特征（例如抗性或除草剂），并通过重组DNA技术生产。",
            "distractors": ["being", "creature", "life form"]
        },
        {
            "keyword": "insertion",
            "original_text": "Experiments, conducted by Pusztai showed that potatoes modified by the insertion of the gene of the snowdrop lectin (an insecticidal proteins), stunted the growth of rats, significantly affected some of their vital organs, including the kidneys, thymus, gastrocnemius muscle and others (1998) and damaged their intestines and their immune system (Ewen and Pusztai, 1999).",
            "translation": "普兹泰（Pusztai）进行的实验表明，通过插入雪花莲凝集素（一种杀虫蛋白）基因而改良的土豆会阻碍大量的生长，对它们的一些重要器官，包括肾脏、胸腺、肺肠肌等产生显著影响（1998年），并且会损害它们的肠道及其免疫系统（欧文（Ewen）和普兹泰，1999年）。",
            "distractors": ["introduction", "incorporation", "implantation"]
        },
        {
            "keyword": "maturity",
            "original_text": "The animals were brought up to sexual maturity on laboratory rat feed.",
            "translation": "这些动物用实验室鼠饲料被培养到性成熟。",
            "distractors": ["adulthood", "ripeness", "development"]
        },
        {
            "keyword": "construct",
            "original_text": "Another group females (3) were allocated to the control group, but their diet was supplemented with the same amount of soya flour, prepared from the traditional soya in which only traces(0.08+0.04%) of the GM construct was present, most likely resulting from cross-contamination.",
            "translation": "另一组雌性大鼠（3只）被分配到对照组，但它们的饮食中添加了相同数量的大豆粉，来自传统大豆，其中仅含有微量(0.08+0.04%)的转基因构建体，很可能是交叉污染的结果。",
            "distractors": ["structure", "formation", "assembly"]
        },
        {
            "keyword": "pregnant",
            "original_text": "Foreign DNA, orally ingested by pregnant mice, was discovered in blood spleen, liver, heart, brain, testes and other organs of foetuses and newborn animals.",
            "translation": "经孕鼠口服的外源DNA在胎儿和新生动物的血液、脾脏、肝脏、心脏、大脑、睾丸和其他器官中发现。",
            "distractors": ["expectant", "gestating", "gravid"]
        },
        {
            "keyword": "pest",
            "original_text": "The term genetically modified organism (GMOs) refers to plants, microbes and animals with genes transferred from other species in order to produce certain novel characteristics (for example resistance to pests, or herbicides) and are produced by recombinant DNA technology.",
            "translation": "转基因生物（GMOs）'指的是那些通过重组DNA技术从其他物种转移基因以产生某些新特性（例如抗虫性或抗除草剂）的植物、微生物和动物。",
            "distractors": ["insect", "vermin", "bug"]
        },
        {
            "keyword": "vitally",
            "original_text": "To understand what effect they can have on us and on our animals it is vitally important to study the influence of these GM plants in different organisms for several generations.",
            "translation": "为了了解它们对我们的动物有什么影响，研究这些转基因植物在不同生物体内几代的影响至关重要。",
            "distractors": ["crucially", "essentially", "imperatively"]
        },
        {
            "keyword": "feed",
            "original_text": "Therefore females only got the standard laboratory feed without any supplementation, although it is acknowledged that the energy and protein content of this diet was less than in the other two groups.",
            "translation": "因此雌鼠只能得到标准的实验饲料没有任何补充，尽管人们认识到这种饲料的能量和蛋白质含量低于其他两组。",
            "distractors": ["food", "nourishment", "diet"]
        },
        {
            "keyword": "portion",
            "original_text": "All rats ate their soya portions well",
            "translation": "所有老鼠都把大豆吃得很好",
            "distractors": ["share", "allotment", "helping"]
        },
        {
            "keyword": "residue",
            "original_text": "Secondly, the accumulation of Roundup residues in GM soya residues could produce negative effect of GM.",
            "translation": "其次，转基因大豆中农作物残留量的积累可产生转基因的负面效应。",
            "distractors": ["remnant", "remainder", "leftover"]
        },
        {
            "keyword": "trace",
            "original_text": "Another group females (3) were allocated to the control group, but their diet was supplemented with the same amount of soya flour, prepared from the traditional soya in which only traces (0.08-0.04%) of the GM construct was present most likely resulting from cross-contamination.",
            "translation": "另外一组（3只）雌性动物被分配到对照组，但它们的饮食中添加了等量的大豆粉，这些大豆粉由传统大豆制成，",
            "distractors": ["hint", "vestige", "speck"]
        },
        {
            "keyword": "reproductive",
            "original_text": "However, there is a lack of investigations into the influence of GM crops on mammals, especially on their reproductive function.",
            "translation": "然而，缺乏对转基因作物对哺乳动物影响的调查，特别是对其生殖功能的影响。",
            "distractors": ["procreative", "generative", "breeding"]
        },
        {
            "keyword": "accumulation",
            "original_text": "Secondly, the accumulation of Roundup residues in GM soya residues could produce negative effect of GM",
            "translation": "其次，转基因大豆残留中农作物残留的积累会产生转基因的负面效应。",
            "distractors": ["build-up", "collection", "amassment"]
        },
        {
            "keyword": "mortality",
            "original_text": "The level of mortality was analyzed by one-way ANOVA, using the Newman-Keuls test for share distribution",
            "translation": "通过单因素方差分析对死亡率水平进行了分析，并使用Newman-Keuls检验对分布进行了比较。",
            "distractors": ["death", "fatality", "loss"]
        },
        {
            "keyword": "lethality",
            "original_text": "The level of lethality was analyzed in the experiment.",
            "translation": "在实验中分析了致死率水平。",
            "distractors": ["deadliness", "fatalness", "mortality"]
        },
        {
            "keyword": "speculate",
            "original_text": "Our data allow us to speculate and presume that the negative effect of GM soya on the newborn pups could be explained by two possible factors.",
            "translation": "我们的数据使我们能够推测和假设，转基因大豆对新生幼崽的负面影响可以通过两个可能因素来解释。",
            "distractors": ["conjecture", "theorize", "hypothesize"]
        },
        {
            "keyword": "internal",
            "original_text": "This fact indicated that the pups from the GM group were the same age as others, but changes occurred with the development of internal organs.",
            "translation": "这一事实表明，转基因组的幼崽与其他幼崽年龄相同，但随着内脏器官的发育而发生变化。",
            "distractors": ["inner", "inside", "interior"]
        },
        {
            "keyword": "infection",
            "original_text": "In order to avoid infection of females, the sperm count and quality had not been determined.",
            "translation": "为了避免雌性感染，精子数量和质量还未进行确定。",
            "distractors": ["contagion", "disease", "infestation"]
        },
        {
            "keyword": "optimally",
            "original_text": "They should have a better chance to grow optimally, unless the amount, and/or the quality of the milk were not affected by consuming the GM soya flour.",
            "translation": "它们应该有更好的机会实现最佳成长，除非食用转基因大豆粉不会影响牛羊肉的数量和质量。",
            "distractors": ["ideally", "perfectly", "excellently"]
        },
        {
            "keyword": "fragment",
            "original_text": "Experimental researches in mice showed that ingested foreign DNA can persist in fragmented form in the gastrointestinal tract, penetrate the intestinal wall, and reach the nuclei of leukocytes, spleen and liver cells (Schubbert et al. 1994).",
            "translation": "实验研究表明，摄入的外源DNA可以以碎片形式在消化道中存留，穿过肠壁，并到达白细胞、脾脏和肝细胞的细胞核(Schubbert等，1994年)",
            "distractors": ["piece", "segment", "portion"]
        },
        {
            "keyword": "penetrate",
            "original_text": "Experimental researches in mice showed that ingested foreign DNA can persist in fragmented form in the gastrointestinal tract, penetrate the intestinal wall, and reach the nuclei of leukocytes, spleen and liver cells (Schubbert et al. 1994).",
            "translation": "实验研究表明，摄入的外源DNA可以以碎片形式在消化道中存留，穿过肠壁，并到达白细胞、脾脏和肝细胞的细胞核(Schubbert等，1994年)",
            "distractors": ["enter", "pierce", "permeate"]
        },
        {
            "keyword": "wean",
            "original_text": "However, unlike the experiments of Brake and Evenson (2004) who started to feed pregnant mice, in our experiments the diets supplemented with GM or traditional soya flours were already given to the female rats 2 weeks before mating already, and we continued to treat them with their respective diet until the pups were weaned.",
            "translation": "然而，与Brake和Evenson(2004)开始喂食怀孕的母鼠的实验不同，在我们的实验中，补充GM或传统大豆粉的饮食已经在交配前两周给予雌性大鼠，我们继续用它们各自的饮食对待它们，直到幼期新奶。",
            "distractors": ["detach", "separate", "disengage"]
        },
        {
            "keyword": "contamination",
            "original_text": "Another group females (3) were allocated to the control group, but their diet was supplemented with the same amount of soya flour, prepared from the traditional soya in which only traces(0.08+0.04%) of the GM construct was present, most likely resulting from cross-contamination",
            "translation": "另一组女性（3人）被分配到对照组，但她们的饮食中添加了相同数量的大豆粉，这种大豆粉是从传统大豆中制备的，其中仅含有微量（0.08+0.04%）的转基因构建体，这很可能是由于交叉污染所致。",
            "distractors": ["pollution", "impurity", "taint"]
        }
    ],
    "Unit 5": [
        {
            "keyword": "coauthor",
            "original_text": "The public awareness of scientific fraud has increased remarkably since the late 1980s when a controversy made front-page news, a controversy about a paper investigated for fraud which had as coauthor a Nobel laureate.",
            "translation": "自20世纪80年代以来，公众对科学欺诈的认识显著提高，当时一场关于一篇因欺诈而被调查的论文的争议成为头版新闻，该论文的含蓄者是诺贝尔奖获得者。",
            "distractors": ["collaborator", "contributor", "partner"]
        },
        {
            "keyword": "consequential",
            "original_text": "However, the clandestine character and consequential lack of reliable information make it difficult to study scientific fraud.",
            "translation": "然而，科学造假的秘密性和由此导致的可靠信息的缺乏，给科学造假的研究带来了困难。",
            "distractors": ["resultant", "ensuing", "subsequent"]
        },
        {
            "keyword": "anonymous",
            "original_text": "In April 1998 a questionnaire designed for anonymous response was mailed to all members with an accompanying letter inviting participation in the survey.",
            "translation": "在1998年4月，我们向所有成员邮寄了一份专为匿名回答而设计的问卷，并附有一封邀请参与调查的信。",
            "distractors": ["unnamed", "unidentified", "incognito"]
        },
        {
            "keyword": "methodological",
            "original_text": "In addition, they have the methodological competence to detect fraud and could be expected to have a special professional interest in the validity of results.",
            "translation": "此外，他们具有检测欺诈的方法能力，并且可以期望他们对结果的有效性具有特殊的专业兴趣。",
            "distractors": ["procedural", "systematic", "technical"]
        },
        {
            "keyword": "prior",
            "original_text": "Prior to the actual survey the questionnaire was pilot-tested on a small number of ISCB nonmember biostatisticians in the United States and in the European Union and was revised in accordance with the experiences from this pilot study.",
            "translation": "在实际调查之前，该问卷在美国和欧盟的少数ISCB非成员生物统计学家中进行了试点测试，并根据该试点研究的经验进行了修订。",
            "distractors": ["previous", "earlier", "preceding"]
        },
        {
            "keyword": "fraudulent",
            "original_text": "The sign test was used to evaluate the difference in the subjectively estimated prevalence of fraudulent projects between epidemiological papers and papers from clinical trials.",
            "translation": "使用符号测试来评估流行病学论文和临床试验论文之",
            "distractors": ["deceitful", "dishonest", "bogus"]
        },
        {
            "keyword": "anonymity",
            "original_text": "Several responders expressed their concern about anonymity (nationality, age, and sex could identify them).",
            "translation": "同主观估计的欺诈项目流行率的差异。",
            "distractors": ["namelessness", "privacy", "confidentiality"]
        },
        {
            "keyword": "ambiguous",
            "original_text": "However, our instructions might have been ambiguous, and we cannot be sure that the responders were not overzealous in what they considered to be fraud.",
            "translation": "几位回应者表达了对匿名性的担忧（国籍、年龄和性别可能会暴露他们的身份）。",
            "distractors": ["unclear", "vague", "equivocal"]
        },
        {
            "keyword": "proximity",
            "original_text": "81 responders (51%) knew of at least one fraudulent project in their proximity during the last 10 years.",
            "translation": "然而，我们的指示可能是模棱两可的，我们不能确定响应者是否对他们认为的欺诈行为过于热心。",
            "distractors": ["closeness", "nearness", "vicinity"]
        },
        {
            "keyword": "vicinity",
            "original_text": "Even if these 81 responses included all episodes of fraud known to the 442 ISCB members, the prevalence estimate of ISCB members knowing of fraudulent projects in their vicinity in the past 10 years would be 18%.",
            "translation": "81名回应者（占比51%）表示，在过去10年里，他们知道自己周边至少有一个欺诈项目。",
            "distractors": ["surroundings", "neighborhood", "locality"]
        },
        {
            "keyword": "falsification",
            "original_text": "43 responses indicated that the fraud had been related to fabrication or falsification of data and 31 to suppression or analysis and deceptive reporting of results",
            "translation": "即使这81个回答中包含了所有由442名国际计算生物学学会（ISCB）成员所知的欺诈事件，在过去10年中，ISCB成员知道在他们周围有欺诈项目的发生率估计约为18%。",
            "distractors": ["forgery", "distortion", "manipulation"]
        },
        {
            "keyword": "suppression",
            "original_text": "43 responses indicated that the fraud had been related to fabrication or falsification of data and 31 to suppression or selective deletion of data, whereas 16 and 32 indicated deceptive designer analysis and deceptive reporting of",
            "translation": "43份反馈表明欺诈行为与数据的编造和伪造有关，31份反馈表明欺诈行为与对结果的隐瞒、分析及欺骗性报告有关。",
            "distractors": ["concealment", "withholding", "repression"]
        },
        {
            "keyword": "confidential",
            "original_text": "Biostatisticians are often privy to confidential data and are knowledgeable enough to understand their implications.",
            "translation": "生物统计学家通常了解机密数据，并有足够的知识来理解其含义。",
            "distractors": ["secret", "private", "classified"]
        },
        {
            "keyword": "collaborator",
            "original_text": "Second, because of their technical knowledge, biostatisticians may be harsh judges of scientific collaborators' optimistic interpretation of data.",
            "translation": "其次，由于他们的技术知识，生物统计学家可能会对科学合作者对数据的乐观解释做出严厉的评判。",
            "distractors": ["partner", "associate", "colleague"]
        },
        {
            "keyword": "respondent",
            "original_text": "However, our instructions might have been ambiguous, and we cannot be sure that the responders were not overzealous in what they considered to be fraud. Third, we cannot be certain that the reported episodes of fraud were at all important, or that the same episode was not reported by multiple respondents.",
            "translation": "然而，我们的指示可能是模棱两可的，我们不能确定响应者在他们认为是欺诈的情况下没有过分热心。第三，我们不能确定报告的欺诈事件是否重要，或者同一事件没有被多个受访者报告。",
            "distractors": ["participant", "answerer", "interviewee"]
        },
        {
            "keyword": "occurrence",
            "original_text": "There are several explanations for the high proportion of responders who knew of the occurrence of fraud, other than the low (37%) response rate.",
            "translation": "除了低比例的应答者(37%)之外，对于知道发生诈骗的应答者比例很高且几种解释。",
            "distractors": ["incidence", "happening", "event"]
        },
        {
            "keyword": "privy",
            "original_text": "Biostatisticians are often privy to confidential data and are knowledgeable enough to understand their implications.",
            "translation": "生物统计学家通常了解机密数据，并且知识渊博，能够理解其含义",
            "distractors": ["informed", "aware", "acquainted"]
        },
        {
            "keyword": "prepublication",
            "original_text": "Therefore they may be in a unique position to observe scientific transactions in the prepublication stages.",
            "translation": "因此，在出版前阶段，他们可能处于观察科学教育的独特地位。",
            "distractors": ["preprint", "before publication", "prior to release"]
        },
        {
            "keyword": "overzealous",
            "original_text": "However, our instructions might have been ambiguous, and we cannot be sure that the responders were not overzealous in what they considered to be fraud.",
            "translation": "然而，我们的说明可能不太明确，我们不能确定受访者是否对他们认为的欺诈行为过于热心。",
            "distractors": ["excessive", "overenthusiastic", "fanatical"]
        },
        {
            "keyword": "implication",
            "original_text": "Biostatisticians are often privy to confidential data and are knowledgeable enough to understand their implications.",
            "translation": "生物统计学家通常了解机密数据，并有足够的知识来理解其含义。",
            "distractors": ["consequence", "significance", "ramification"]
        },
        {
            "keyword": "reiterate",
            "original_text": "The low proportion of biostatisticians who reported working for organizations with systems for handling suspected fraud reiterates the need for more such systems.",
            "translation": "生物统计学家报告说，他们工作的组织中有处理可疑欺诈的系统的比例很低，这再次表明需要更多这样的系统。",
            "distractors": ["repeat", "restate", "reemphasize"]
        },
        {
            "keyword": "proportion",
            "original_text": "Although the overall low response rate to this survey limits its generalizability, the high proportion of respondents knowing about fraudulent projects provided the primary motivation for this report.",
            "translation": "虽然该调查的总体低回复率限制了其普遍性，但高比例的受访者了解欺诈项目提供了本报告的主要动机。",
            "distractors": ["percentage", "ratio", "fraction"]
        },
        {
            "keyword": "prevalent",
            "original_text": "However, our survey seems to suggest that fraud might be more prevalent in epidemiological studies than in clinical trials.",
            "translation": "然而，我们的调查似乎表明，欺诈行为在流行病学研究中比在临床试验中可能更为普遍。",
            "distractors": ["common", "widespread", "pervasive"]
        },
        {
            "keyword": "amenable",
            "original_text": "A possible explanation for this finding may be the more controlled nature of the clinical trial, which makes it less amenable to fraud.",
            "translation": "对这一发现的一个可能解释可能是临床试验的控制性更强，这使得它不太容易受到欺诈。",
            "distractors": ["responsive", "receptive", "susceptible"]
        }
    ]
}



class QuizManager:
    def __init__(self):
        self.current_session = {}

    def start_unit_quiz(self, unit_name):
        """开始单元练习"""
        questions = question_bank.get(unit_name, [])
        return {
            'unit_name': unit_name,
            'questions': questions,
            'current_index': 0,
            'score': 0,
            'total_answered': 0,
            'question_order': list(range(len(questions)))
        }

    def start_mixed_quiz(self):
        """开始乱序练习"""
        all_questions = []
        for unit_name, questions in question_bank.items():
            for q in questions:
                q_copy = q.copy()
                q_copy['unit'] = unit_name
                all_questions.append(q_copy)

        random.shuffle(all_questions)
        return {
            'unit_name': '所有单元混合',
            'questions': all_questions,
            'current_index': 0,
            'score': 0,
            'total_answered': 0,
            'question_order': list(range(len(all_questions)))
        }

    def get_current_question(self, session_data):
        """获取当前题目"""
        if not session_data or session_data['current_index'] >= len(session_data['questions']):
            return None

        current_q = session_data['questions'][session_data['current_index']]
        options = current_q['distractors'] + [current_q['keyword']]
        random.shuffle(options)

        return {
            'question_number': session_data['current_index'] + 1,
            'total_questions': len(session_data['questions']),
            'unit_name': session_data['unit_name'],
            'original_text': self.create_blank_text(current_q),
            'options': options,
            'keyword': current_q['keyword'],
            'translation': current_q['translation'],
            'full_text': current_q['original_text']
        }

    def create_blank_text(self, question_data):
        """创建带空白的文本"""
        keyword = question_data["keyword"]
        original_text = question_data["original_text"]
        return original_text.replace(keyword, "————")

    def check_answer(self, session_data, user_answer):
        """检查答案"""
        current_q = session_data['questions'][session_data['current_index']]
        is_correct = (user_answer == current_q['keyword'])

        if is_correct:
            session_data['score'] += 1
        session_data['total_answered'] += 1
        session_data['current_index'] += 1

        return {
            'is_correct': is_correct,
            'correct_answer': current_q['keyword'],
            'user_answer': user_answer,
            'translation': current_q['translation'],
            'full_text': current_q['original_text'],
            'score': session_data['score'],
            'total_answered': session_data['total_answered'],
            'has_next': session_data['current_index'] < len(session_data['questions'])
        }


quiz_manager = QuizManager()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/start_unit/<unit_name>')
def start_unit(unit_name):
    session_data = quiz_manager.start_unit_quiz(unit_name)
    question = quiz_manager.get_current_question(session_data)
    return jsonify({
        'session_data': session_data,
        'question': question
    })


@app.route('/api/start_mixed')
def start_mixed():
    session_data = quiz_manager.start_mixed_quiz()
    question = quiz_manager.get_current_question(session_data)
    return jsonify({
        'session_data': session_data,
        'question': question
    })


@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    session_data = data['session_data']
    user_answer = data['user_answer']

    result = quiz_manager.check_answer(session_data, user_answer)
    next_question = None
    if result['has_next']:
        next_question = quiz_manager.get_current_question(session_data)

    return jsonify({
        'result': result,
        'next_question': next_question,
        'session_data': session_data
    })


@app.route('/api/get_units')
def get_units():
    units = {}
    for unit_name, questions in question_bank.items():
        units[unit_name] = len(questions)
    return jsonify(units)


if __name__ == '__main__':
    # 获取环境变量中的端口，如果没有则使用5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)