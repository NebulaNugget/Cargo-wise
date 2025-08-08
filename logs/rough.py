<?xml version="1.0" encoding="UTF-8"?>
<robot generator="Robot 7.3 (Python 3.11.0 on win32)" generated="2025-08-07T13:05:31.009983" rpa="false" schemaversion="5">
<suite id="s1" name="Tmpipc78 J2" source="C:\Users\UK-PC\AppData\Local\Temp\tmpipc78_j2.robot">
<test id="s1-t1" name="Execute Sikuli Task" line="15">
<kw name="Initialize Sikuli Environment" type="SETUP">
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-07T13:05:38.310323" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.9920001029968 seconds left.</msg>
<msg time="2025-08-07T13:05:38.313317" level="INFO">Initializing Sikuli environment</msg>
<arg>Initializing Sikuli environment</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-07T13:05:38.307313" elapsed="0.006004"/>
</kw>
<kw name="Set Library Search Order" owner="BuiltIn">
<msg time="2025-08-07T13:05:38.314333" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.9879894256592 seconds left.</msg>
<arg>Sikuli</arg>
<doc>Sets the resolution order to use when a name matches multiple keywords.</doc>
<status status="PASS" start="2025-08-07T13:05:38.313317" elapsed="0.001999"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:05:38.316329" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.9859938621521 seconds left.</msg>
<arg>Starting Sikuli Process...</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:05:38.315316" elapsed="0.002007"/>
</kw>
<kw name="Start Sikuli Process" owner="Sikuli">
<msg time="2025-08-07T13:05:38.318324" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.98399901390076 seconds left.</msg>
<msg time="2025-08-07T13:05:38.320318" level="DEBUG">Free TCP port is: 55944</msg>
<msg time="2025-08-07T13:05:38.324318" level="INFO">Starting process:
java -jar "C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\venv\Lib\site-packages\SikuliLibrary\lib\SikuliLibrary.jar" 55944 C:\Users\UK-PC\AppData\Local\Temp\tmpaim8y68i</msg>
<msg time="2025-08-07T13:05:38.324318" level="DEBUG">Process configuration:
cwd:     C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend
shell:   True
stdout:  C:\Users\UK-PC\AppData\Local\Temp\tmpaim8y68i\Sikuli_java_stdout_1754568338.3223178.txt
stderr:  C:\Users\UK-PC\AppData\Local\Temp\tmpaim8y68i\Sikuli_java_stderr_1754568338.3223178.txt
stdin:   None
alias:   None
env:     None</msg>
<msg time="2025-08-07T13:05:38.345322" level="INFO">Start sikuli java process on port 55944</msg>
<msg time="2025-08-07T13:05:41.535687" level="INFO">Sikuli java process is started</msg>
<status status="PASS" start="2025-08-07T13:05:38.317323" elapsed="6.806189"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:05:45.124506" level="DEBUG">Test timeout 5 minutes 30 seconds active. 323.1778163909912 seconds left.</msg>
<arg>Adding image path: ${IMAGE_DIR}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:05:45.124506" elapsed="0.004005"/>
</kw>
<kw name="Add Image Path" owner="Sikuli">
<msg time="2025-08-07T13:05:45.129504" level="DEBUG">Test timeout 5 minutes 30 seconds active. 323.17281889915466 seconds left.</msg>
<arg>${IMAGE_DIR}</arg>
<doc>Add image path</doc>
<status status="PASS" start="2025-08-07T13:05:45.129504" elapsed="0.088009"/>
</kw>
<kw name="Set Move Mouse Delay" owner="Sikuli">
<msg time="2025-08-07T13:05:45.218513" level="DEBUG">Test timeout 5 minutes 30 seconds active. 323.0838100910187 seconds left.</msg>
<arg>0.5</arg>
<doc>Set move mouse delay</doc>
<status status="PASS" start="2025-08-07T13:05:45.218513" elapsed="0.028006"/>
</kw>
<kw name="Set Min Similarity" owner="Sikuli">
<msg time="2025-08-07T13:05:45.247519" level="DEBUG">Test timeout 5 minutes 30 seconds active. 323.05480432510376 seconds left.</msg>
<arg>0.5</arg>
<doc>Set min similarity (accuracy of matching elements).</doc>
<status status="PASS" start="2025-08-07T13:05:45.246519" elapsed="0.018998"/>
</kw>
<kw name="Run Keyword If" owner="BuiltIn">
<kw name="Launch CargoWise Application">
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-07T13:05:45.268502" level="DEBUG">Test timeout 5 minutes 30 seconds active. 323.03382110595703 seconds left.</msg>
<msg time="2025-08-07T13:05:45.269505" level="INFO">Launching application from: C:\Program Files (x86)\WiseTech Global\WiseCloud Client\WiseCloudClient.exe</msg>
<arg>Launching application from: ${APP_PATH}</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-07T13:05:45.268502" elapsed="0.001003"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:05:45.270508" level="DEBUG">Test timeout 5 minutes 30 seconds active. 323.03181529045105 seconds left.</msg>
<arg>Launching application: ${APP_PATH}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:05:45.269505" elapsed="0.001998"/>
</kw>
<kw name="Start Process" owner="Process">
<msg time="2025-08-07T13:05:45.272514" level="DEBUG">Test timeout 5 minutes 30 seconds active. 323.0298089981079 seconds left.</msg>
<msg time="2025-08-07T13:05:45.273501" level="INFO">Starting process:
C:\Program Files (x86)\WiseTech Global\WiseCloud Client\WiseCloudClient.exe</msg>
<msg time="2025-08-07T13:05:45.273501" level="DEBUG">Process configuration:
cwd:     C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend
shell:   True
stdout:  PIPE
stderr:  PIPE
stdin:   None
alias:   None
env:     None</msg>
<msg time="2025-08-07T13:05:45.288504" level="INFO">${process} = &lt;Popen: returncode: None args: 'C:\\Program Files (x86)\\WiseTech Global\\Wi...&gt;</msg>
<var>${process}</var>
<arg>${APP_PATH}</arg>
<arg>shell=True</arg>
<doc>Starts a new process on background.</doc>
<status status="PASS" start="2025-08-07T13:05:45.271503" elapsed="0.017001"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-07T13:05:45.289501" level="DEBUG">Test timeout 5 minutes 30 seconds active. 323.0128216743469 seconds left.</msg>
<msg time="2025-08-07T13:05:45.292510" level="INFO">${timestamp} = 2025-08-07 13:05:45.292</msg>
<var>${timestamp}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-07T13:05:45.289501" elapsed="0.003009"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:05:45.293521" level="DEBUG">Test timeout 5 minutes 30 seconds active. 323.0088016986847 seconds left.</msg>
<arg>Application launch initiated at ${timestamp}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:05:45.292510" elapsed="0.002003"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-07T13:05:45.295507" level="DEBUG">Test timeout 5 minutes 30 seconds active. 323.0068154335022 seconds left.</msg>
<msg time="2025-08-07T13:06:00.297895" level="INFO">Slept 15 seconds.</msg>
<arg>15s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-07T13:05:45.295507" elapsed="15.003393"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:06:00.299984" level="DEBUG">Test timeout 5 minutes 30 seconds active. 308.0023384094238 seconds left.</msg>
<arg>Application should be started now</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:06:00.298900" elapsed="0.002989"/>
</kw>
<doc>Launch the CargoWise application</doc>
<status status="PASS" start="2025-08-07T13:05:45.267512" elapsed="15.034377"/>
</kw>
<arg>'${APP_PATH}' != '${EMPTY}'</arg>
<arg>Launch CargoWise Application</arg>
<doc>Runs the given keyword with the given arguments, if ``condition`` is true.</doc>
<status status="PASS" start="2025-08-07T13:05:45.266501" elapsed="15.035388"/>
</kw>
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-07T13:06:00.302983" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.99934005737305 seconds left.</msg>
<msg time="2025-08-07T13:06:00.304888" level="INFO">Sikuli environment initialized</msg>
<arg>Sikuli environment initialized</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-07T13:06:00.302983" elapsed="0.001905"/>
</kw>
<doc>Initialize Sikuli with minimal settings</doc>
<status status="PASS" start="2025-08-07T13:05:38.304319" elapsed="22.000569"/>
</kw>
<kw name="Run Keyword And Continue On Failure" owner="BuiltIn">
<kw name="Execute Task With Progress Logging">
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-07T13:06:00.309895" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.99242782592773 seconds left.</msg>
<msg time="2025-08-07T13:06:00.312207" level="INFO">${start_time} = 2025-08-07 13:06:00.311</msg>
<var>${start_time}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-07T13:06:00.308890" elapsed="0.003317"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:06:00.313109" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.98921394348145 seconds left.</msg>
<arg>Task execution started at ${start_time}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:06:00.313109" elapsed="0.002000"/>
</kw>
<kw name="Run Keyword And Return Status" owner="BuiltIn">
<kw name="Run Keyword With Timeout">
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:06:00.319112" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.9832110404968 seconds left.</msg>
<arg>Running keyword with timeout: ${keyword} (${timeout})</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:06:00.318108" elapsed="0.002999"/>
</kw>
<kw name="Run Keyword And Return Status" owner="BuiltIn">
<kw name="Wait Until Keyword Succeeds" owner="BuiltIn">
<kw name="Run Sikuli Task">
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-07T13:06:00.326138" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.9761846065521 seconds left.</msg>
<msg time="2025-08-07T13:06:00.327105" level="INFO">Starting Sikuli task execution</msg>
<arg>Starting Sikuli task execution</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-07T13:06:00.326138" elapsed="0.000967"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:06:00.328282" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.97404050827026 seconds left.</msg>
<arg>Executing Sikuli task...</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:06:00.327105" elapsed="0.003001"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-07T13:06:00.331274" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.97104930877686 seconds left.</msg>
<msg time="2025-08-07T13:06:00.332101" level="INFO">${task_start} = 2025-08-07 13:06:00.331</msg>
<var>${task_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-07T13:06:00.330106" elapsed="0.001995"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:06:00.333273" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.96904945373535 seconds left.</msg>
<arg>Task started at ${task_start}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:06:00.332101" elapsed="0.001998"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:06:00.335273" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.9670498371124 seconds left.</msg>
<arg>Step 1: Input Text</arg>
<arg>${IMAGE_DIR}/search-shipment.png</arg>
<arg>${HOUSEBILL}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:06:00.334099" elapsed="0.001999"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-07T13:06:00.337272" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.96505069732666 seconds left.</msg>
<msg time="2025-08-07T13:06:00.338100" level="INFO">${step1_start} = 2025-08-07 13:06:00.337</msg>
<var>${step1_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-07T13:06:00.336098" elapsed="0.002002"/>
</kw>
<kw name="Input Text" owner="Sikuli">
<msg time="2025-08-07T13:06:00.339275" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.9630482196808 seconds left.</msg>
<msg time="2025-08-07T13:06:04.076852" level="INFO">Input Text:
A2B00001667</msg>
<msg time="2025-08-07T13:06:04.076852" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpaim8y68i\sikuli_captured\sikuliximage-1754568361471.png</msg>
<msg time="2025-08-07T13:06:04.076852" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1754568361471.png'/&gt;
[log] CLICK on L[484,51]@S(0) (633 msec)
[log]  TYPE "A2B00001667"</msg>
<arg>${IMAGE_DIR}/search-shipment.png</arg>
<arg>${HOUSEBILL}</arg>
<doc>Input text.
 Image could be empty</doc>
<status status="PASS" start="2025-08-07T13:06:00.338100" elapsed="3.738752"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-07T13:06:04.077847" level="DEBUG">Test timeout 5 minutes 30 seconds active. 304.2244756221771 seconds left.</msg>
<msg time="2025-08-07T13:06:04.078863" level="INFO">${timestamp} = 20250807_130604</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-07T13:06:04.076852" elapsed="0.002011"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-07T13:06:04.079981" level="DEBUG">Test timeout 5 minutes 30 seconds active. 304.22234177589417 seconds left.</msg>
<msg time="2025-08-07T13:06:04.080841" level="INFO">${screenshot_name} = step_1_20250807_130604.png</msg>
<var>${screenshot_name}</var>
<arg>step_1_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-07T13:06:04.078863" elapsed="0.001978"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-07T13:06:04.081847" level="DEBUG">Test timeout 5 minutes 30 seconds active. 304.2204761505127 seconds left.</msg>
<msg time="2025-08-07T13:06:04.082836" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ca97ee33-be00-4954-80cc-69e5aba02495/step_1_20250807_130604.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-07T13:06:04.081847" elapsed="0.000989"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-07T13:06:04.083848" level="DEBUG">Test timeout 5 minutes 30 seconds active. 304.2184751033783 seconds left.</msg>
<msg time="2025-08-07T13:06:04.084838" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ca97ee33-be00-4954-80cc-69e5aba02495"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ca97ee33-be00-4954-80cc-69e5aba02495&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-07T13:06:04.082836" elapsed="0.002002"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-07T13:06:04.085848" level="DEBUG">Test timeout 5 minutes 30 seconds active. 304.2164750099182 seconds left.</msg>
<msg time="2025-08-07T13:06:04.351694" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpaim8y68i\sikuli_captured\sikuliximage-1754568364151.png</msg>
<msg time="2025-08-07T13:06:04.351694" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1754568364151.png'/&gt;</msg>
<msg time="2025-08-07T13:06:04.352696" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpaim8y68i\sikuli_captured\sikuliximage-1754568364151.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-07T13:06:04.084838" elapsed="0.267858"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-07T13:06:04.353728" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.94859504699707 seconds left.</msg>
<msg time="2025-08-07T13:06:04.386705" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpaim8y68i\sikuli_captured\sikuliximage-1754568364151.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpaim8y68i\sikuli_captured\sikuliximage-1754568364151.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ca97ee33-be00-4954-80cc-69e5aba02495\step_1_20250807_130604.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ca97ee33-be00-4954-80cc-69e5aba02495\step_1_20250807_130604.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-07T13:06:04.352696" elapsed="0.035012"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:06:04.388711" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.91361141204834 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:06:04.387708" elapsed="0.003009"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-07T13:06:04.390717" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.91061091423035 seconds left.</msg>
<msg time="2025-08-07T13:06:04.392806" level="INFO">${step1_end} = 2025-08-07 13:06:04.392</msg>
<var>${step1_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-07T13:06:04.390717" elapsed="0.002089"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-07T13:06:04.393845" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.9084777832031 seconds left.</msg>
<msg time="2025-08-07T13:06:04.403701" level="INFO">${step1_duration} = 4.055</msg>
<var>${step1_duration}</var>
<arg>${step1_end}</arg>
<arg>${step1_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-07T13:06:04.392806" elapsed="0.010895"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:06:04.404712" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.89761114120483 seconds left.</msg>
<arg>Step 1 completed in ${step1_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:06:04.403701" elapsed="0.002569"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-07T13:06:04.406270" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.8960530757904 seconds left.</msg>
<msg time="2025-08-07T13:06:06.408177" level="INFO">Slept 2 seconds.</msg>
<arg>2s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-07T13:06:04.406270" elapsed="2.001907"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-07T13:06:06.409038" level="DEBUG">Test timeout 5 minutes 30 seconds active. 301.89328479766846 seconds left.</msg>
<arg>Step 2: Type</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-07T13:06:06.408177" elapsed="0.001855"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-07T13:06:06.410032" level="DEBUG">Test timeout 5 minutes 30 seconds active. 301.89229106903076 seconds left.</msg>
<msg time="2025-08-07T13:06:06.411053" level="INFO">${step2_start} = 2025-08-07 13:06:06.411</msg>
<var>${step2_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-07T13:06:06.410032" elapsed="0.002000"/>
</kw>
<kw name="Type">
<msg time="2025-08-07T13:06:06.414550" level="FAIL">No keyword with name 'Type' found.</msg>
<status status="FAIL" start="2025-08-07T13:06:06.414033" elapsed="0.000517">No keyword with name 'Type' found.</status>
</kw>
<kw name="Get Current Date" owner="DateTime">
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="NOT RUN" start="2025-08-07T13:06:06.414550" elapsed="0.000000"/>
</kw>