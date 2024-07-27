## This file contains all the prompts in the form of python dictionaries

plot_ideas_prompt = """

Task: Your job is to help generate ideas for graphical plots on a certain topic using different chart styles and variables and their combinations. The plots should {p_level}. Return the output as a list of JSON objects of key-value pairs, one for each graph.

Instructions: Generate ideas for plots on the topic of {plot_topic} in the following format:

1. Key: "chart_type"
   Value: The chart type, for example "line chart", "bar chart", "scatter plot", "violin plot", "heatmap", "box plot", "contour plot", "bubble chart", "histogram", or other type of plot.

2. Key: "variables"
   Value: A list of variables involved in the plot, for example "age", "gender", "height", etc.

3. Key: "x-axis"
   Value: The variable that should be plotted on the x-axis. Leave blank if not applicable to this chart type.

4. Key: "y-axis"
   Value: The variable that should be plotted on the y-axis. Leave blank if not applicable to this chart type.

5. Key: "color"
   Value: The variable that should be used to color the data points. Leave blank if not applicable to this chart type.

6. Key: "style"
   Value: The variable that should be used to represent the style of the categories (e.g. solid, dashed, dotted, shading). Leave blank if not applicable to this chart type.

7. Key: "label"
   Value: The variable that should be used to label the data points. Leave blank if not applicable to this chart type.

8. Key: "sizes"
   Value: The variable that should be used to define the sizes of the data points. Leave blank if not applicable to this chart type.

9. Key: "error_bars"
   Value: True or False. Leave blank if not applicable to this chart type.

10. Key: "instructions"
   Value: Additional instructions in natural language that are required to accurately specify the chart appearance.

Do not return anything except the list of JSON objects of key-value pairs as output.

""".strip()



plot_create_prompt = """

Task: Your job is to generate a plot according to the instructions and JSON schema provided. If you do not have access to the data required for it, you should generate hypothetical data that seems plausible and reflects realistic trends.

Instructions: {instructions}

Schema: {schema}

Do not return anything except the Python code for the plot as output.

""".strip()



plot_questions_prompt = """

Task: Your job is to generate a multiple choice question to test a user's data literacy level. You will be provided the description and Python code for a data plot and will be asked to generate a question followed by four answer options, one per line, with the correct option marked with a star (*) at the beginning. The question should focus on {q_level}.

Instructions: {instructions}

Code: {code}

Do not return anything except the question and the answer options as output.

""".strip()



question_levels = {
    1: 'the graphical elements of the plot and what they represent for this data',
    2: 'the trends that can be observed in the data from looking at the plot',
    3: 'the insights that can be drawn from the trends in the data and the actions that can be taken based on them'
}



plot_levels = {
    1: 'be of low complexity and use a few graph elements from the list below',
    2: 'be of medium complexity and use some graph elements from the list below',
    3: 'be of high complexity and use most graph elements from the list below'
}



literacy_levels = {
    1: """The user does not know anything about the graphs and charts. The output should explain the fundamental concepts of the graph in question in easy to understand language.
          Name the type of graph, explain the components of the graph, how it is used and why it is used. The user cannot consume technical insights and recommendations. The user will really like to enhance their ability to remember this type of chart.
          Give the user limited insights and recommendations that can be drawn from the graph by applying domain knowledge in an intuitive way. Examples should be added as well according to their domain and role.""",
    2: """The user knows about different kinds of charts but finds it difficult building relationships between variables given in the chart. The output should be less on explaining the graph in question
          rather why it's used here and how to interpret the relationships between the variables. The user will really like to learn how to build relationships between different variables. The output should take into account domain and role.""",
    3: """The user can build relationships between 2 variables but finds it difficult to build relationship between more variables. The output so all the sections should be balanced with knowledge. The output should take into account domain and role""",
    4: """The user can build relationships between more than 2 variables but finds it difficult to apply their domain knowledge on the graph and draw insights so the focus should be on layering in the domain knowledge to the
    graph. The output should take into account domain and role""",
    5: """The user can apply domain knowledge and derive insights and actionables from the graphs. The output should include inter and intra domain informations, market trends,
     questions for user to think about in insights and recommendations section. The further links sections should have further readings as well. The output should take into account domain and role"""
}



content_prompt = """

Task: Your task is to generate helpful educational content around the graph image that is uploaded. The content should be tailored to the individual using them, provided to you as input. The output should be content around the graph broken down into multiple sections.

Instructions: Generate the graph content for the user who has following characteristics. The detail level of the ouput should be dictated by the user's ability.

1. Understands {language} as their preferred language,
2. Have role of {user_role} at their workplace, and the {domain} is the industry they work in.
3. {dl_level}

The output should have the following schema:

1. Key: "graph_description"
   Value: The description of the graph shown in the image.

2. Key: "data_description"
   Value: The description of the labels, axis, colors, legends, data points, error bars.

3. Key: "insights"
   Value: Bullet point wise insights that can be drawn from it given the {domain} as domain and {user_role} as role mentioned.

4- Key: "recommendations"
   Value: The actionables tailored to the their {user_role} as role and {domain} as a domain.

5- Key: "further_links"
   Value: The further references to studies and topics relevant to the graphs, trends.

Do not return anything except the list of JSON objects of key-value pairs as output.

""".strip()
