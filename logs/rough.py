<?xml version="1.0" encoding="UTF-8"?>
<robot generator="Robot 7.3 (Python 3.11.0 on win32)" generated="2025-08-15T14:00:09.887743" rpa="false" schemaversion="5">
<suite id="s1" name="Tmpl3Br725H" source="C:\Users\UK-PC\AppData\Local\Temp\tmpl3br725h.robot">
<test id="s1-t1" name="Execute Sikuli Task" line="15">
<kw name="Initialize Sikuli Environment" type="SETUP">
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-15T14:00:17.500800" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.9829797744751 seconds left.</msg>
<msg time="2025-08-15T14:00:17.514779" level="INFO">Initializing Sikuli environment</msg>
<arg>Initializing Sikuli environment</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-15T14:00:17.493795" elapsed="0.020984"/>
</kw>
<kw name="Set Library Search Order" owner="BuiltIn">
<msg time="2025-08-15T14:00:17.516788" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.96699118614197 seconds left.</msg>
<arg>Sikuli</arg>
<doc>Sets the resolution order to use when a name matches multiple keywords.</doc>
<status status="PASS" start="2025-08-15T14:00:17.514779" elapsed="0.004009"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:17.519788" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.96399092674255 seconds left.</msg>
<arg>Starting Sikuli Process...</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:17.519788" elapsed="0.003992"/>
</kw>
<kw name="Start Sikuli Process" owner="Sikuli">
<msg time="2025-08-15T14:00:17.524797" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.9589822292328 seconds left.</msg>
<msg time="2025-08-15T14:00:17.531778" level="DEBUG">Free TCP port is: 60379</msg>
<msg time="2025-08-15T14:00:17.535778" level="INFO">Starting process:
java -jar "C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\venv\Lib\site-packages\SikuliLibrary\lib\SikuliLibrary.jar" 60379 C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm</msg>
<msg time="2025-08-15T14:00:17.535778" level="DEBUG">Process configuration:
cwd:     C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend
shell:   True
stdout:  C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\Sikuli_java_stdout_1755262817.5337842.txt
stderr:  C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\Sikuli_java_stderr_1755262817.5337842.txt
stdin:   None
alias:   None
env:     None</msg>
<msg time="2025-08-15T14:00:17.555782" level="INFO">Start sikuli java process on port 60379</msg>
<msg time="2025-08-15T14:00:20.831993" level="INFO">Sikuli java process is started</msg>
<status status="PASS" start="2025-08-15T14:00:17.524797" elapsed="7.613128"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:25.139917" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.3438618183136 seconds left.</msg>
<arg>Adding image path: ${IMAGE_DIR}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:25.138929" elapsed="0.005993"/>
</kw>
<kw name="Add Image Path" owner="Sikuli">
<msg time="2025-08-15T14:00:25.145935" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.3378441333771 seconds left.</msg>
<arg>${IMAGE_DIR}</arg>
<doc>Add image path</doc>
<status status="PASS" start="2025-08-15T14:00:25.145935" elapsed="0.109983"/>
</kw>
<kw name="Set Move Mouse Delay" owner="Sikuli">
<msg time="2025-08-15T14:00:25.257027" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.2267518043518 seconds left.</msg>
<arg>0.5</arg>
<doc>Set move mouse delay</doc>
<status status="PASS" start="2025-08-15T14:00:25.255918" elapsed="0.033028"/>
</kw>
<kw name="Set Min Similarity" owner="Sikuli">
<msg time="2025-08-15T14:00:25.289941" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.19383788108826 seconds left.</msg>
<arg>0.5</arg>
<doc>Set min similarity (accuracy of matching elements).</doc>
<status status="PASS" start="2025-08-15T14:00:25.289941" elapsed="0.015981"/>
</kw>
<kw name="Run Keyword If" owner="BuiltIn">
<kw name="Launch CargoWise Application">
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-15T14:00:25.309922" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.17385721206665 seconds left.</msg>
<msg time="2025-08-15T14:00:25.310908" level="INFO">Launching application from: C:\Program Files (x86)\WiseTech Global\WiseCloud Client\WiseCloudClient.exe</msg>
<arg>Launching application from: ${APP_PATH}</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-15T14:00:25.308920" elapsed="0.001988"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:25.311917" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.17186188697815 seconds left.</msg>
<arg>Launching application: ${APP_PATH}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:25.310908" elapsed="0.002002"/>
</kw>
<kw name="Start Process" owner="Process">
<msg time="2025-08-15T14:00:25.313921" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.16985845565796 seconds left.</msg>
<msg time="2025-08-15T14:00:25.314915" level="INFO">Starting process:
C:\Program Files (x86)\WiseTech Global\WiseCloud Client\WiseCloudClient.exe</msg>
<msg time="2025-08-15T14:00:25.314915" level="DEBUG">Process configuration:
cwd:     C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend
shell:   True
stdout:  PIPE
stderr:  PIPE
stdin:   None
alias:   None
env:     None</msg>
<msg time="2025-08-15T14:00:25.332912" level="INFO">${process} = &lt;Popen: returncode: None args: 'C:\\Program Files (x86)\\WiseTech Global\\Wi...&gt;</msg>
<var>${process}</var>
<arg>${APP_PATH}</arg>
<arg>shell=True</arg>
<doc>Starts a new process on background.</doc>
<status status="PASS" start="2025-08-15T14:00:25.312910" elapsed="0.020002"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:25.333912" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.1498670578003 seconds left.</msg>
<msg time="2025-08-15T14:00:25.337917" level="INFO">${timestamp} = 2025-08-15 14:00:25.337</msg>
<var>${timestamp}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:25.333912" elapsed="0.004005"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:25.339290" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.14448952674866 seconds left.</msg>
<arg>Application launch initiated at ${timestamp}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:25.337917" elapsed="0.005000"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:00:25.343914" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.13986468315125 seconds left.</msg>
<msg time="2025-08-15T14:00:40.346757" level="INFO">Slept 15 seconds.</msg>
<arg>15s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:00:25.342917" elapsed="15.004829"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.348762" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.13501715660095 seconds left.</msg>
<arg>Application should be started now</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:40.347746" elapsed="0.012015"/>
</kw>
<doc>Launch the CargoWise application</doc>
<status status="PASS" start="2025-08-15T14:00:25.308920" elapsed="15.050841"/>
</kw>
<arg>'${APP_PATH}' != '${EMPTY}'</arg>
<arg>Launch CargoWise Application</arg>
<doc>Runs the given keyword with the given arguments, if ``condition`` is true.</doc>
<status status="PASS" start="2025-08-15T14:00:25.306921" elapsed="15.052840"/>
</kw>
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.360756" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.1230237483978 seconds left.</msg>
<msg time="2025-08-15T14:00:40.368766" level="INFO">Sikuli environment initialized</msg>
<arg>Sikuli environment initialized</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-15T14:00:40.360756" elapsed="0.008995"/>
</kw>
<doc>Initialize Sikuli with minimal settings</doc>
<status status="PASS" start="2025-08-15T14:00:17.487845" elapsed="22.881906"/>
</kw>
<kw name="Run Keyword And Continue On Failure" owner="BuiltIn">
<kw name="Execute Task With Progress Logging">
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:40.372755" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.11102414131165 seconds left.</msg>
<msg time="2025-08-15T14:00:40.381770" level="INFO">${start_time} = 2025-08-15 14:00:40.380</msg>
<var>${start_time}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:40.372755" elapsed="0.009015"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.382737" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.10104179382324 seconds left.</msg>
<arg>Task execution started at ${start_time}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:40.381770" elapsed="0.002981"/>
</kw>
<kw name="Run Keyword And Return Status" owner="BuiltIn">
<kw name="Run Keyword With Timeout">
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.388758" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.0950217247009 seconds left.</msg>
<arg>Running keyword with timeout: ${keyword} (${timeout})</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:40.387758" elapsed="0.001992"/>
</kw>
<kw name="Run Keyword And Return Status" owner="BuiltIn">
<kw name="Wait Until Keyword Succeeds" owner="BuiltIn">
<kw name="Run Sikuli Task">
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.396751" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.0870280265808 seconds left.</msg>
<msg time="2025-08-15T14:00:40.397739" level="INFO">Starting Sikuli task execution</msg>
<arg>Starting Sikuli task execution</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-15T14:00:40.395744" elapsed="0.003007"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.398751" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.0850279331207 seconds left.</msg>
<arg>Executing Sikuli task...</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:40.398751" elapsed="0.001998"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:40.401750" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.08202958106995 seconds left.</msg>
<msg time="2025-08-15T14:00:40.402746" level="INFO">${task_start} = 2025-08-15 14:00:40.402</msg>
<var>${task_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:40.400749" elapsed="0.001997"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.403759" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.0800199508667 seconds left.</msg>
<arg>Task started at ${task_start}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:40.403759" elapsed="0.002253"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.407053" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.07672595977783 seconds left.</msg>
<arg>Step 1: # Click New Order</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:40.406012" elapsed="0.002025"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:40.409060" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.07471895217896 seconds left.</msg>
<msg time="2025-08-15T14:00:40.410036" level="INFO">${step1_start} = 2025-08-15 14:00:40.409</msg>
<var>${step1_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:40.408037" elapsed="0.001999"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:40.411071" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.0727081298828 seconds left.</msg>
<msg time="2025-08-15T14:00:40.412036" level="INFO">${timestamp} = 20250815_140040</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:40.410036" elapsed="0.002000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.413068" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.07071113586426 seconds left.</msg>
<msg time="2025-08-15T14:00:40.415072" level="INFO">${screenshot_name} = step_1_20250815_140040.png</msg>
<var>${screenshot_name}</var>
<arg>step_1_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:00:40.412036" elapsed="0.003036"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.416056" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.0677230358124 seconds left.</msg>
<msg time="2025-08-15T14:00:40.446037" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_1_20250815_140040.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:00:40.415072" elapsed="0.030965"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:00:40.447056" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.0367238521576 seconds left.</msg>
<msg time="2025-08-15T14:00:40.467037" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:00:40.446037" elapsed="0.022008"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:00:40.469054" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.0147249698639 seconds left.</msg>
<msg time="2025-08-15T14:00:40.844156" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262840590.png</msg>
<msg time="2025-08-15T14:00:40.844156" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262840590.png'/&gt;</msg>
<msg time="2025-08-15T14:00:40.845166" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262840590.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:00:40.468045" elapsed="0.377121"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:00:40.846155" level="DEBUG">Test timeout 5 minutes 30 seconds active. 306.6376247406006 seconds left.</msg>
<msg time="2025-08-15T14:00:40.876151" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262840590.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262840590.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_1_20250815_140040.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_1_20250815_140040.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:00:40.845166" elapsed="0.031981"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.877147" level="DEBUG">Test timeout 5 minutes 30 seconds active. 306.606632232666 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:40.877147" elapsed="0.001002"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:40.879143" level="DEBUG">Test timeout 5 minutes 30 seconds active. 306.6046359539032 seconds left.</msg>
<msg time="2025-08-15T14:00:40.880153" level="INFO">${step1_end} = 2025-08-15 14:00:40.880</msg>
<var>${step1_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:40.879143" elapsed="0.001010"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:00:40.881280" level="DEBUG">Test timeout 5 minutes 30 seconds active. 306.60249948501587 seconds left.</msg>
<msg time="2025-08-15T14:00:40.894286" level="INFO">${step1_duration} = 0.471</msg>
<var>${step1_duration}</var>
<arg>${step1_end}</arg>
<arg>${step1_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:00:40.881280" elapsed="0.013006"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.895287" level="DEBUG">Test timeout 5 minutes 30 seconds active. 306.58849239349365 seconds left.</msg>
<arg>Step 1 completed in ${step1_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:40.894286" elapsed="0.001864"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:40.897150" level="DEBUG">Test timeout 5 minutes 30 seconds active. 306.58662939071655 seconds left.</msg>
<arg>Step 2: Click</arg>
<arg>${IMAGE_DIR}/operate-btn.png</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:40.896150" elapsed="0.002117"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:40.899280" level="DEBUG">Test timeout 5 minutes 30 seconds active. 306.58449935913086 seconds left.</msg>
<msg time="2025-08-15T14:00:40.900152" level="INFO">${step2_start} = 2025-08-15 14:00:40.900</msg>
<var>${step2_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:40.899280" elapsed="0.000872"/>
</kw>
<kw name="Click" owner="Sikuli">
<msg time="2025-08-15T14:00:40.901148" level="DEBUG">Test timeout 5 minutes 30 seconds active. 306.582631111145 seconds left.</msg>
<msg time="2025-08-15T14:00:43.720353" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262842598.png</msg>
<msg time="2025-08-15T14:00:43.720353" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262842598.png'/&gt;
[log] CLICK on L[56,57]@S(0) (626 msec)</msg>
<arg>${IMAGE_DIR}/operate-btn.png</arg>
<doc>Click</doc>
<status status="PASS" start="2025-08-15T14:00:40.901148" elapsed="2.819205"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:43.721367" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.76241183280945 seconds left.</msg>
<msg time="2025-08-15T14:00:43.727443" level="INFO">${timestamp} = 20250815_140043</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:43.720353" elapsed="0.007090"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:00:43.727981" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.75579833984375 seconds left.</msg>
<msg time="2025-08-15T14:00:43.730013" level="INFO">${screenshot_name} = step_2_20250815_140043.png</msg>
<var>${screenshot_name}</var>
<arg>step_2_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:00:43.727981" elapsed="0.002032"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:00:43.731032" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.75274682044983 seconds left.</msg>
<msg time="2025-08-15T14:00:43.732017" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_2_20250815_140043.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:00:43.730013" elapsed="0.002004"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:00:43.733043" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.7507367134094 seconds left.</msg>
<msg time="2025-08-15T14:00:43.735017" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:00:43.733043" elapsed="0.001974"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:00:43.736030" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.7477488517761 seconds left.</msg>
<msg time="2025-08-15T14:00:43.978803" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262843819.png</msg>
<msg time="2025-08-15T14:00:43.978803" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262843819.png'/&gt;</msg>
<msg time="2025-08-15T14:00:43.978803" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262843819.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:00:43.735017" elapsed="0.243786"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:00:43.979804" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.5039749145508 seconds left.</msg>
<msg time="2025-08-15T14:00:44.022817" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262843819.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262843819.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_2_20250815_140043.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_2_20250815_140043.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:00:43.978803" elapsed="0.045002"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:44.024817" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.4589626789093 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:44.024817" elapsed="0.009985"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:44.035809" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.4479703903198 seconds left.</msg>
<msg time="2025-08-15T14:00:44.038804" level="INFO">${step2_end} = 2025-08-15 14:00:44.039</msg>
<var>${step2_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:44.035809" elapsed="0.003997"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:00:44.039806" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.44397354125977 seconds left.</msg>
<msg time="2025-08-15T14:00:44.041800" level="INFO">${step2_duration} = 3.139</msg>
<var>${step2_duration}</var>
<arg>${step2_end}</arg>
<arg>${step2_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:00:44.039806" elapsed="0.001994"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:44.042803" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.4409761428833 seconds left.</msg>
<arg>Step 2 completed in ${step2_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:44.041800" elapsed="0.001999"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:00:44.044798" level="DEBUG">Test timeout 5 minutes 30 seconds active. 303.43898153305054 seconds left.</msg>
<msg time="2025-08-15T14:00:47.045020" level="INFO">Slept 3 seconds.</msg>
<arg>3s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:00:44.043799" elapsed="3.001221"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:47.046020" level="DEBUG">Test timeout 5 minutes 30 seconds active. 300.4377591609955 seconds left.</msg>
<arg>Step 3: Click</arg>
<arg>${IMAGE_DIR}/forwarding-btn.png</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:47.045020" elapsed="0.012984"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:47.059017" level="DEBUG">Test timeout 5 minutes 30 seconds active. 300.4247624874115 seconds left.</msg>
<msg time="2025-08-15T14:00:47.070015" level="INFO">${step3_start} = 2025-08-15 14:00:47.070</msg>
<var>${step3_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:47.059017" elapsed="0.010998"/>
</kw>
<kw name="Click" owner="Sikuli">
<msg time="2025-08-15T14:00:47.071027" level="DEBUG">Test timeout 5 minutes 30 seconds active. 300.41275238990784 seconds left.</msg>
<msg time="2025-08-15T14:00:48.453553" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262847484.png</msg>
<msg time="2025-08-15T14:00:48.453553" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262847484.png'/&gt;
[log] CLICK on L[98,138]@S(0) (604 msec)</msg>
<arg>${IMAGE_DIR}/forwarding-btn.png</arg>
<doc>Click</doc>
<status status="PASS" start="2025-08-15T14:00:47.071027" elapsed="1.383513"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:48.456541" level="DEBUG">Test timeout 5 minutes 30 seconds active. 299.02723836898804 seconds left.</msg>
<msg time="2025-08-15T14:00:48.457524" level="INFO">${timestamp} = 20250815_140048</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:48.454540" elapsed="0.002984"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:00:48.458537" level="DEBUG">Test timeout 5 minutes 30 seconds active. 299.02524280548096 seconds left.</msg>
<msg time="2025-08-15T14:00:48.459522" level="INFO">${screenshot_name} = step_3_20250815_140048.png</msg>
<var>${screenshot_name}</var>
<arg>step_3_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:00:48.457524" elapsed="0.001998"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:00:48.460530" level="DEBUG">Test timeout 5 minutes 30 seconds active. 299.02324891090393 seconds left.</msg>
<msg time="2025-08-15T14:00:48.462566" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_3_20250815_140048.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:00:48.459522" elapsed="0.003044"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:00:48.463664" level="DEBUG">Test timeout 5 minutes 30 seconds active. 299.02011466026306 seconds left.</msg>
<msg time="2025-08-15T14:00:48.466536" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:00:48.462566" elapsed="0.003970"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:00:48.467638" level="DEBUG">Test timeout 5 minutes 30 seconds active. 299.0161409378052 seconds left.</msg>
<msg time="2025-08-15T14:00:48.644967" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262848544.png</msg>
<msg time="2025-08-15T14:00:48.644967" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262848544.png'/&gt;</msg>
<msg time="2025-08-15T14:00:48.644967" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262848544.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:00:48.466536" elapsed="0.178431"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:00:48.645959" level="DEBUG">Test timeout 5 minutes 30 seconds active. 298.83782029151917 seconds left.</msg>
<msg time="2025-08-15T14:00:48.674567" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262848544.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262848544.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_3_20250815_140048.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_3_20250815_140048.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:00:48.645959" elapsed="0.028608"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:48.675567" level="DEBUG">Test timeout 5 minutes 30 seconds active. 298.8082118034363 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:48.675567" elapsed="0.000991"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:48.677554" level="DEBUG">Test timeout 5 minutes 30 seconds active. 298.8062255382538 seconds left.</msg>
<msg time="2025-08-15T14:00:48.678553" level="INFO">${step3_end} = 2025-08-15 14:00:48.679</msg>
<var>${step3_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:48.677554" elapsed="0.000999"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:00:48.679546" level="DEBUG">Test timeout 5 minutes 30 seconds active. 298.80423283576965 seconds left.</msg>
<msg time="2025-08-15T14:00:48.680555" level="INFO">${step3_duration} = 1.609</msg>
<var>${step3_duration}</var>
<arg>${step3_end}</arg>
<arg>${step3_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:00:48.678553" elapsed="0.002002"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:48.681563" level="DEBUG">Test timeout 5 minutes 30 seconds active. 298.8022162914276 seconds left.</msg>
<arg>Step 3 completed in ${step3_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:48.680555" elapsed="0.002037"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:00:48.683556" level="DEBUG">Test timeout 5 minutes 30 seconds active. 298.8002235889435 seconds left.</msg>
<msg time="2025-08-15T14:00:51.684923" level="INFO">Slept 3 seconds.</msg>
<arg>3s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:00:48.683556" elapsed="3.001367"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:51.686984" level="DEBUG">Test timeout 5 minutes 30 seconds active. 295.796795129776 seconds left.</msg>
<arg>Step 4: Click</arg>
<arg>${IMAGE_DIR}/order.png</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:51.685973" elapsed="0.003002"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:51.690075" level="DEBUG">Test timeout 5 minutes 30 seconds active. 295.7937045097351 seconds left.</msg>
<msg time="2025-08-15T14:00:51.691981" level="INFO">${step4_start} = 2025-08-15 14:00:51.691</msg>
<var>${step4_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:51.690075" elapsed="0.001906"/>
</kw>
<kw name="Click" owner="Sikuli">
<msg time="2025-08-15T14:00:51.693058" level="DEBUG">Test timeout 5 minutes 30 seconds active. 295.79072093963623 seconds left.</msg>
<msg time="2025-08-15T14:00:52.998398" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262852058.png</msg>
<msg time="2025-08-15T14:00:52.998398" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262852058.png'/&gt;
[log] CLICK on L[643,428]@S(0) (647 msec)</msg>
<arg>${IMAGE_DIR}/order.png</arg>
<doc>Click</doc>
<status status="PASS" start="2025-08-15T14:00:51.693058" elapsed="1.306334"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:52.999392" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.4843873977661 seconds left.</msg>
<msg time="2025-08-15T14:00:53.001392" level="INFO">${timestamp} = 20250815_140053</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:52.999392" elapsed="0.002000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:00:53.001392" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.48238706588745 seconds left.</msg>
<msg time="2025-08-15T14:00:53.002542" level="INFO">${screenshot_name} = step_4_20250815_140053.png</msg>
<var>${screenshot_name}</var>
<arg>step_4_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:00:53.001392" elapsed="0.002016"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:00:53.003408" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.48037123680115 seconds left.</msg>
<msg time="2025-08-15T14:00:53.004420" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_4_20250815_140053.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:00:53.003408" elapsed="0.001012"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:00:53.005394" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.4783854484558 seconds left.</msg>
<msg time="2025-08-15T14:00:53.006387" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:00:53.005394" elapsed="0.000993"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:00:53.007390" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.4763889312744 seconds left.</msg>
<msg time="2025-08-15T14:00:53.180668" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262853090.png</msg>
<msg time="2025-08-15T14:00:53.180668" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262853090.png'/&gt;</msg>
<msg time="2025-08-15T14:00:53.181675" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262853090.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:00:53.007390" elapsed="0.174285"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:00:53.181675" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.3021047115326 seconds left.</msg>
<msg time="2025-08-15T14:00:53.211667" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262853090.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262853090.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_4_20250815_140053.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_4_20250815_140053.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:00:53.181675" elapsed="0.030987"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:53.212662" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.27111768722534 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:53.212662" elapsed="0.002007"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:00:53.215662" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.26811718940735 seconds left.</msg>
<msg time="2025-08-15T14:00:53.216660" level="INFO">${step4_end} = 2025-08-15 14:00:53.217</msg>
<var>${step4_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:00:53.214669" elapsed="0.001991"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:00:53.217655" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.2661247253418 seconds left.</msg>
<msg time="2025-08-15T14:00:53.218659" level="INFO">${step4_duration} = 1.526</msg>
<var>${step4_duration}</var>
<arg>${step4_end}</arg>
<arg>${step4_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:00:53.216660" elapsed="0.001999"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:00:53.219668" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.26411151885986 seconds left.</msg>
<arg>Step 4 completed in ${step4_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:00:53.218659" elapsed="0.002013"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:00:53.221810" level="DEBUG">Test timeout 5 minutes 30 seconds active. 294.26196908950806 seconds left.</msg>
<msg time="2025-08-15T14:01:00.223067" level="INFO">Slept 7 seconds.</msg>
<arg>7s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:00:53.220672" elapsed="7.002395"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:00.225117" level="DEBUG">Test timeout 5 minutes 30 seconds active. 287.2586622238159 seconds left.</msg>
<arg>Step 5: Click</arg>
<arg>${IMAGE_DIR}/new-btn.png</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:00.224106" elapsed="0.001992"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:00.228105" level="DEBUG">Test timeout 5 minutes 30 seconds active. 287.25567412376404 seconds left.</msg>
<msg time="2025-08-15T14:01:00.231108" level="INFO">${step5_start} = 2025-08-15 14:01:00.230</msg>
<var>${step5_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:00.228105" elapsed="0.003003"/>
</kw>
<kw name="Click" owner="Sikuli">
<msg time="2025-08-15T14:01:00.232107" level="DEBUG">Test timeout 5 minutes 30 seconds active. 287.2516722679138 seconds left.</msg>
<msg time="2025-08-15T14:01:01.494600" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262860616.png</msg>
<msg time="2025-08-15T14:01:01.494600" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262860616.png'/&gt;
[log] CLICK on L[226,226]@S(0) (610 msec)</msg>
<arg>${IMAGE_DIR}/new-btn.png</arg>
<doc>Click</doc>
<status status="PASS" start="2025-08-15T14:01:00.231108" elapsed="1.263492"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:01.495607" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.9881718158722 seconds left.</msg>
<msg time="2025-08-15T14:01:01.496599" level="INFO">${timestamp} = 20250815_140101</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:01.495607" elapsed="0.000992"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:01.497597" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.98618245124817 seconds left.</msg>
<msg time="2025-08-15T14:01:01.498597" level="INFO">${screenshot_name} = step_5_20250815_140101.png</msg>
<var>${screenshot_name}</var>
<arg>step_5_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:01.497597" elapsed="0.001000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:01.499595" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.9841845035553 seconds left.</msg>
<msg time="2025-08-15T14:01:01.501615" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_5_20250815_140101.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:01.499595" elapsed="0.002020"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:01:01.501615" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.98216438293457 seconds left.</msg>
<msg time="2025-08-15T14:01:01.503597" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:01:01.501615" elapsed="0.001982"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:01:01.503597" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.9801824092865 seconds left.</msg>
<msg time="2025-08-15T14:01:01.680102" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262861585.png</msg>
<msg time="2025-08-15T14:01:01.680102" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262861585.png'/&gt;</msg>
<msg time="2025-08-15T14:01:01.681102" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262861585.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:01:01.503597" elapsed="0.177505"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:01:01.682108" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.8016712665558 seconds left.</msg>
<msg time="2025-08-15T14:01:01.715096" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262861585.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262861585.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_5_20250815_140101.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_5_20250815_140101.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:01:01.681102" elapsed="0.035005"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:01.716107" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.76767230033875 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:01.716107" elapsed="0.001993"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:01.718100" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.7656788825989 seconds left.</msg>
<msg time="2025-08-15T14:01:01.720093" level="INFO">${step5_end} = 2025-08-15 14:01:01.719</msg>
<var>${step5_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:01.718100" elapsed="0.001993"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:01:01.721099" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.76268005371094 seconds left.</msg>
<msg time="2025-08-15T14:01:01.722094" level="INFO">${step5_duration} = 1.489</msg>
<var>${step5_duration}</var>
<arg>${step5_end}</arg>
<arg>${step5_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:01:01.720093" elapsed="0.002001"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:01.723090" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.760689496994 seconds left.</msg>
<arg>Step 5 completed in ${step5_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:01.723090" elapsed="0.001001"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:01:01.725088" level="DEBUG">Test timeout 5 minutes 30 seconds active. 285.7586908340454 seconds left.</msg>
<msg time="2025-08-15T14:01:08.727727" level="INFO">Slept 7 seconds.</msg>
<arg>7s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:01:01.725088" elapsed="7.002639"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:08.728736" level="DEBUG">Test timeout 5 minutes 30 seconds active. 278.7550437450409 seconds left.</msg>
<arg>Step 6: Input Text</arg>
<arg>${IMAGE_DIR}/order-buyer.png</arg>
<arg>${BUYER}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:08.727727" elapsed="0.002997"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:08.731739" level="DEBUG">Test timeout 5 minutes 30 seconds active. 278.75204062461853 seconds left.</msg>
<msg time="2025-08-15T14:01:08.732731" level="INFO">${step6_start} = 2025-08-15 14:01:08.733</msg>
<var>${step6_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:08.731739" elapsed="0.000992"/>
</kw>
<kw name="Input Text" owner="Sikuli">
<msg time="2025-08-15T14:01:08.733734" level="DEBUG">Test timeout 5 minutes 30 seconds active. 278.75004482269287 seconds left.</msg>
<msg time="2025-08-15T14:01:11.455101" level="INFO">Input Text:
luclenliv</msg>
<msg time="2025-08-15T14:01:11.455101" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262869112.png</msg>
<msg time="2025-08-15T14:01:11.455101" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262869112.png'/&gt;
[log] CLICK on L[50,90]@S(0) (607 msec)
[log]  TYPE "luclenliv"</msg>
<arg>${IMAGE_DIR}/order-buyer.png</arg>
<arg>${BUYER}</arg>
<doc>Input text.
 Image could be empty</doc>
<status status="PASS" start="2025-08-15T14:01:08.732731" elapsed="2.722370"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:11.456096" level="DEBUG">Test timeout 5 minutes 30 seconds active. 276.02768325805664 seconds left.</msg>
<msg time="2025-08-15T14:01:11.457104" level="INFO">${timestamp} = 20250815_140111</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:11.456096" elapsed="0.001008"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:11.458090" level="DEBUG">Test timeout 5 minutes 30 seconds active. 276.02568912506104 seconds left.</msg>
<msg time="2025-08-15T14:01:11.459091" level="INFO">${screenshot_name} = step_6_20250815_140111.png</msg>
<var>${screenshot_name}</var>
<arg>step_6_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:11.458090" elapsed="0.001001"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:11.460104" level="DEBUG">Test timeout 5 minutes 30 seconds active. 276.02367544174194 seconds left.</msg>
<msg time="2025-08-15T14:01:11.461099" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_6_20250815_140111.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:11.459091" elapsed="0.002008"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:01:11.462089" level="DEBUG">Test timeout 5 minutes 30 seconds active. 276.02169036865234 seconds left.</msg>
<msg time="2025-08-15T14:01:11.463090" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:01:11.461099" elapsed="0.001991"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:01:11.464088" level="DEBUG">Test timeout 5 minutes 30 seconds active. 276.01969146728516 seconds left.</msg>
<msg time="2025-08-15T14:01:11.630404" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262871545.png</msg>
<msg time="2025-08-15T14:01:11.630404" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262871545.png'/&gt;</msg>
<msg time="2025-08-15T14:01:11.631399" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262871545.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:01:11.463090" elapsed="0.168309"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:01:11.631399" level="DEBUG">Test timeout 5 minutes 30 seconds active. 275.85238003730774 seconds left.</msg>
<msg time="2025-08-15T14:01:11.659413" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262871545.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262871545.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_6_20250815_140111.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_6_20250815_140111.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:01:11.631399" elapsed="0.028014"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:11.660409" level="DEBUG">Test timeout 5 minutes 30 seconds active. 275.823370218277 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:11.660409" elapsed="0.001996"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:11.663394" level="DEBUG">Test timeout 5 minutes 30 seconds active. 275.82038474082947 seconds left.</msg>
<msg time="2025-08-15T14:01:11.665389" level="INFO">${step6_end} = 2025-08-15 14:01:11.664</msg>
<var>${step6_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:11.663394" elapsed="0.001995"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:01:11.666396" level="DEBUG">Test timeout 5 minutes 30 seconds active. 275.81738328933716 seconds left.</msg>
<msg time="2025-08-15T14:01:11.667389" level="INFO">${step6_duration} = 2.931</msg>
<var>${step6_duration}</var>
<arg>${step6_end}</arg>
<arg>${step6_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:01:11.665389" elapsed="0.002000"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:11.668408" level="DEBUG">Test timeout 5 minutes 30 seconds active. 275.8153715133667 seconds left.</msg>
<arg>Step 6 completed in ${step6_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:11.668408" elapsed="0.000979"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:01:11.670397" level="DEBUG">Test timeout 5 minutes 30 seconds active. 275.8133821487427 seconds left.</msg>
<msg time="2025-08-15T14:01:14.672280" level="INFO">Slept 3 seconds.</msg>
<arg>3s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:01:11.669387" elapsed="3.002893"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:14.673296" level="DEBUG">Test timeout 5 minutes 30 seconds active. 272.81048345565796 seconds left.</msg>
<arg>Step 7: Input Text</arg>
<arg>${IMAGE_DIR}/order-supplier.png</arg>
<arg>${SUPPLIER}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:14.672280" elapsed="0.002003"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:14.675293" level="DEBUG">Test timeout 5 minutes 30 seconds active. 272.80848598480225 seconds left.</msg>
<msg time="2025-08-15T14:01:14.676282" level="INFO">${step7_start} = 2025-08-15 14:01:14.676</msg>
<var>${step7_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:14.675293" elapsed="0.000989"/>
</kw>
<kw name="Input Text" owner="Sikuli">
<msg time="2025-08-15T14:01:14.677293" level="DEBUG">Test timeout 5 minutes 30 seconds active. 272.80648589134216 seconds left.</msg>
<msg time="2025-08-15T14:01:17.134017" level="INFO">Input Text:
a2bempsyd</msg>
<msg time="2025-08-15T14:01:17.134017" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262875100.png</msg>
<msg time="2025-08-15T14:01:17.134017" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262875100.png'/&gt;
[log] CLICK on L[53,251]@S(0) (604 msec)
[log]  TYPE "a2bempsyd"</msg>
<arg>${IMAGE_DIR}/order-supplier.png</arg>
<arg>${SUPPLIER}</arg>
<doc>Input text.
 Image could be empty</doc>
<status status="PASS" start="2025-08-15T14:01:14.676282" elapsed="2.457735"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:17.134017" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.3497624397278 seconds left.</msg>
<msg time="2025-08-15T14:01:17.134017" level="INFO">${timestamp} = 20250815_140117</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:17.134017" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:17.134017" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.3497624397278 seconds left.</msg>
<msg time="2025-08-15T14:01:17.134017" level="INFO">${screenshot_name} = step_7_20250815_140117.png</msg>
<var>${screenshot_name}</var>
<arg>step_7_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:17.134017" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:17.134017" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.3497624397278 seconds left.</msg>
<msg time="2025-08-15T14:01:17.134017" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_7_20250815_140117.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:17.134017" elapsed="0.000000"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:01:17.143587" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.34019207954407 seconds left.</msg>
<msg time="2025-08-15T14:01:17.143587" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:01:17.143587" elapsed="0.000000"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:01:17.143587" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.34019207954407 seconds left.</msg>
<msg time="2025-08-15T14:01:17.334423" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262877234.png</msg>
<msg time="2025-08-15T14:01:17.334423" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262877234.png'/&gt;</msg>
<msg time="2025-08-15T14:01:17.334423" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262877234.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:01:17.143587" elapsed="0.190836"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:01:17.334423" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.1493558883667 seconds left.</msg>
<msg time="2025-08-15T14:01:17.374277" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262877234.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262877234.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_7_20250815_140117.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_7_20250815_140117.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:01:17.334423" elapsed="0.039854"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:17.374277" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.10950231552124 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:17.374277" elapsed="0.000000"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:17.384299" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.0994801521301 seconds left.</msg>
<msg time="2025-08-15T14:01:17.386031" level="INFO">${step7_end} = 2025-08-15 14:01:17.386</msg>
<var>${step7_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:17.374277" elapsed="0.011754"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:01:17.386031" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.0977478027344 seconds left.</msg>
<msg time="2025-08-15T14:01:17.386031" level="INFO">${step7_duration} = 2.71</msg>
<var>${step7_duration}</var>
<arg>${step7_end}</arg>
<arg>${step7_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:01:17.386031" elapsed="0.000000"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:17.386031" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.0977478027344 seconds left.</msg>
<arg>Step 7 completed in ${step7_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:17.386031" elapsed="0.000000"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:01:17.386031" level="DEBUG">Test timeout 5 minutes 30 seconds active. 270.0977478027344 seconds left.</msg>
<msg time="2025-08-15T14:01:20.394595" level="INFO">Slept 3 seconds.</msg>
<arg>3s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:01:17.386031" elapsed="3.008564"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:20.394595" level="DEBUG">Test timeout 5 minutes 30 seconds active. 267.0891840457916 seconds left.</msg>
<arg>Step 8: Click</arg>
<arg>${IMAGE_DIR}/order-additional-detail.png</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:20.394595" elapsed="0.000000"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:20.394595" level="DEBUG">Test timeout 5 minutes 30 seconds active. 267.0891840457916 seconds left.</msg>
<msg time="2025-08-15T14:01:20.394595" level="INFO">${step8_start} = 2025-08-15 14:01:20.395</msg>
<var>${step8_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:20.394595" elapsed="0.000000"/>
</kw>
<kw name="Click" owner="Sikuli">
<msg time="2025-08-15T14:01:20.394595" level="DEBUG">Test timeout 5 minutes 30 seconds active. 267.0891840457916 seconds left.</msg>
<msg time="2025-08-15T14:01:21.574667" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262880703.png</msg>
<msg time="2025-08-15T14:01:21.574667" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262880703.png'/&gt;
[log] CLICK on L[224,402]@S(0) (604 msec)</msg>
<arg>${IMAGE_DIR}/order-additional-detail.png</arg>
<doc>Click</doc>
<status status="PASS" start="2025-08-15T14:01:20.394595" elapsed="1.180072"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:21.574667" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.9091122150421 seconds left.</msg>
<msg time="2025-08-15T14:01:21.574667" level="INFO">${timestamp} = 20250815_140121</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:21.574667" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:21.574667" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.9091122150421 seconds left.</msg>
<msg time="2025-08-15T14:01:21.581228" level="INFO">${screenshot_name} = step_8_20250815_140121.png</msg>
<var>${screenshot_name}</var>
<arg>step_8_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:21.574667" elapsed="0.006561"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:21.581228" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.90255093574524 seconds left.</msg>
<msg time="2025-08-15T14:01:21.581228" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_8_20250815_140121.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:21.581228" elapsed="0.000000"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:01:21.581228" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.90255093574524 seconds left.</msg>
<msg time="2025-08-15T14:01:21.581228" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:01:21.581228" elapsed="0.000000"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:01:21.591286" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.89249324798584 seconds left.</msg>
<msg time="2025-08-15T14:01:21.763658" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262881672.png</msg>
<msg time="2025-08-15T14:01:21.763658" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262881672.png'/&gt;</msg>
<msg time="2025-08-15T14:01:21.763658" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262881672.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:01:21.581228" elapsed="0.182430"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:01:21.763658" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.72012162208557 seconds left.</msg>
<msg time="2025-08-15T14:01:21.783930" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262881672.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262881672.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_8_20250815_140121.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_8_20250815_140121.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:01:21.763658" elapsed="0.020272"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:21.793793" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.68998646736145 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:21.783930" elapsed="0.009863"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:21.793793" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.68998646736145 seconds left.</msg>
<msg time="2025-08-15T14:01:21.793793" level="INFO">${step8_end} = 2025-08-15 14:01:21.794</msg>
<var>${step8_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:21.793793" elapsed="0.000000"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:01:21.793793" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.68998646736145 seconds left.</msg>
<msg time="2025-08-15T14:01:21.793793" level="INFO">${step8_duration} = 1.399</msg>
<var>${step8_duration}</var>
<arg>${step8_end}</arg>
<arg>${step8_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:01:21.793793" elapsed="0.000000"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:21.793793" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.68998646736145 seconds left.</msg>
<arg>Step 8 completed in ${step8_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:21.793793" elapsed="0.000000"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:01:21.793793" level="DEBUG">Test timeout 5 minutes 30 seconds active. 265.68998646736145 seconds left.</msg>
<msg time="2025-08-15T14:01:23.794575" level="INFO">Slept 2 seconds.</msg>
<arg>2s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:01:21.793793" elapsed="2.000782"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:23.794575" level="DEBUG">Test timeout 5 minutes 30 seconds active. 263.68920373916626 seconds left.</msg>
<arg>Step 9: Input Text</arg>
<arg>${IMAGE_DIR}/order-empty-return-date.png</arg>
<arg>${CONTAINER_RETURN_DATE}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:23.794575" elapsed="0.000000"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:23.794575" level="DEBUG">Test timeout 5 minutes 30 seconds active. 263.68920373916626 seconds left.</msg>
<msg time="2025-08-15T14:01:23.794575" level="INFO">${step9_start} = 2025-08-15 14:01:23.795</msg>
<var>${step9_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:23.794575" elapsed="0.000000"/>
</kw>
<kw name="Input Text" owner="Sikuli">
<msg time="2025-08-15T14:01:23.794575" level="DEBUG">Test timeout 5 minutes 30 seconds active. 263.68920373916626 seconds left.</msg>
<msg time="2025-08-15T14:01:26.051710" level="INFO">Input Text:
15-11-2025</msg>
<msg time="2025-08-15T14:01:26.051710" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262884101.png</msg>
<msg time="2025-08-15T14:01:26.051710" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262884101.png'/&gt;
[log] CLICK on L[181,422]@S(0) (594 msec)
[log]  TYPE "15-11-2025"</msg>
<arg>${IMAGE_DIR}/order-empty-return-date.png</arg>
<arg>${CONTAINER_RETURN_DATE}</arg>
<doc>Input text.
 Image could be empty</doc>
<status status="PASS" start="2025-08-15T14:01:23.794575" elapsed="2.257135"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:26.051710" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.4320697784424 seconds left.</msg>
<msg time="2025-08-15T14:01:26.063639" level="INFO">${timestamp} = 20250815_140126</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:26.051710" elapsed="0.011929"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:26.063639" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.4201407432556 seconds left.</msg>
<msg time="2025-08-15T14:01:26.063639" level="INFO">${screenshot_name} = step_9_20250815_140126.png</msg>
<var>${screenshot_name}</var>
<arg>step_9_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:26.063639" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:26.063639" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.4201407432556 seconds left.</msg>
<msg time="2025-08-15T14:01:26.072866" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_9_20250815_140126.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:26.063639" elapsed="0.009227"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:01:26.072866" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.41091299057007 seconds left.</msg>
<msg time="2025-08-15T14:01:26.072866" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:01:26.072866" elapsed="0.000000"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:01:26.072866" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.41091299057007 seconds left.</msg>
<msg time="2025-08-15T14:01:26.253890" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262886173.png</msg>
<msg time="2025-08-15T14:01:26.253890" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262886173.png'/&gt;</msg>
<msg time="2025-08-15T14:01:26.254156" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262886173.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:01:26.072866" elapsed="0.181290"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:01:26.254766" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.22901344299316 seconds left.</msg>
<msg time="2025-08-15T14:01:26.274726" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262886173.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262886173.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_9_20250815_140126.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_9_20250815_140126.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:01:26.254766" elapsed="0.019960"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:26.274726" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.2090528011322 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:26.274726" elapsed="0.010462"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:26.285188" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.1985914707184 seconds left.</msg>
<msg time="2025-08-15T14:01:26.285188" level="INFO">${step9_end} = 2025-08-15 14:01:26.285</msg>
<var>${step9_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:26.285188" elapsed="0.000000"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:01:26.285188" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.1985914707184 seconds left.</msg>
<msg time="2025-08-15T14:01:26.285188" level="INFO">${step9_duration} = 2.49</msg>
<var>${step9_duration}</var>
<arg>${step9_end}</arg>
<arg>${step9_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:01:26.285188" elapsed="0.000000"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:26.285188" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.1985914707184 seconds left.</msg>
<arg>Step 9 completed in ${step9_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:26.285188" elapsed="0.000000"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:01:26.285188" level="DEBUG">Test timeout 5 minutes 30 seconds active. 261.1985914707184 seconds left.</msg>
<msg time="2025-08-15T14:01:29.286044" level="INFO">Slept 3 seconds.</msg>
<arg>3s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:01:26.285188" elapsed="3.000856"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:29.287292" level="DEBUG">Test timeout 5 minutes 30 seconds active. 258.1964876651764 seconds left.</msg>
<arg>Step 10: Input Text</arg>
<arg>${IMAGE_DIR}/order-sanction.png</arg>
<arg>${SANCTION}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:29.286698" elapsed="0.002015"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:29.289368" level="DEBUG">Test timeout 5 minutes 30 seconds active. 258.19441080093384 seconds left.</msg>
<msg time="2025-08-15T14:01:29.290678" level="INFO">${step10_start} = 2025-08-15 14:01:29.291</msg>
<var>${step10_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:29.289244" elapsed="0.001434"/>
</kw>
<kw name="Input Text" owner="Sikuli">
<msg time="2025-08-15T14:01:29.291799" level="DEBUG">Test timeout 5 minutes 30 seconds active. 258.1919803619385 seconds left.</msg>
<msg time="2025-08-15T14:01:31.421805" level="INFO">Input Text:
approved</msg>
<msg time="2025-08-15T14:01:31.421805" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262889569.png</msg>
<msg time="2025-08-15T14:01:31.421805" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262889569.png'/&gt;
[log] CLICK on L[309,469]@S(0) (604 msec)
[log]  TYPE "approved"</msg>
<arg>${IMAGE_DIR}/order-sanction.png</arg>
<arg>${SANCTION}</arg>
<doc>Input text.
 Image could be empty</doc>
<status status="PASS" start="2025-08-15T14:01:29.291244" elapsed="2.130561"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:31.421805" level="DEBUG">Test timeout 5 minutes 30 seconds active. 256.06197452545166 seconds left.</msg>
<msg time="2025-08-15T14:01:31.421805" level="INFO">${timestamp} = 20250815_140131</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:31.421805" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:31.421805" level="DEBUG">Test timeout 5 minutes 30 seconds active. 256.06197452545166 seconds left.</msg>
<msg time="2025-08-15T14:01:31.431704" level="INFO">${screenshot_name} = step_10_20250815_140131.png</msg>
<var>${screenshot_name}</var>
<arg>step_10_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:31.421805" elapsed="0.009899"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:31.431704" level="DEBUG">Test timeout 5 minutes 30 seconds active. 256.0520749092102 seconds left.</msg>
<msg time="2025-08-15T14:01:31.431704" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_10_20250815_140131.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:31.431704" elapsed="0.000000"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:01:31.431704" level="DEBUG">Test timeout 5 minutes 30 seconds active. 256.0520749092102 seconds left.</msg>
<msg time="2025-08-15T14:01:31.431704" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:01:31.431704" elapsed="0.000000"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:01:31.431704" level="DEBUG">Test timeout 5 minutes 30 seconds active. 256.0520749092102 seconds left.</msg>
<msg time="2025-08-15T14:01:31.603804" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262891532.png</msg>
<msg time="2025-08-15T14:01:31.603804" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262891532.png'/&gt;</msg>
<msg time="2025-08-15T14:01:31.603804" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262891532.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:01:31.431704" elapsed="0.172100"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:01:31.603804" level="DEBUG">Test timeout 5 minutes 30 seconds active. 255.87997484207153 seconds left.</msg>
<msg time="2025-08-15T14:01:31.643816" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262891532.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262891532.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_10_20250815_140131.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_10_20250815_140131.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:01:31.603804" elapsed="0.040012"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:31.643816" level="DEBUG">Test timeout 5 minutes 30 seconds active. 255.8399636745453 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:31.643816" elapsed="0.005427"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:31.653806" level="DEBUG">Test timeout 5 minutes 30 seconds active. 255.8299732208252 seconds left.</msg>
<msg time="2025-08-15T14:01:31.653806" level="INFO">${step10_end} = 2025-08-15 14:01:31.654</msg>
<var>${step10_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:31.649243" elapsed="0.004563"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:01:31.653806" level="DEBUG">Test timeout 5 minutes 30 seconds active. 255.8299732208252 seconds left.</msg>
<msg time="2025-08-15T14:01:31.653806" level="INFO">${step10_duration} = 2.363</msg>
<var>${step10_duration}</var>
<arg>${step10_end}</arg>
<arg>${step10_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:01:31.653806" elapsed="0.000000"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:31.653806" level="DEBUG">Test timeout 5 minutes 30 seconds active. 255.8299732208252 seconds left.</msg>
<arg>Step 10 completed in ${step10_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:31.653806" elapsed="0.010530"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:01:31.664336" level="DEBUG">Test timeout 5 minutes 30 seconds active. 255.81944346427917 seconds left.</msg>
<msg time="2025-08-15T14:01:34.664714" level="INFO">Slept 3 seconds.</msg>
<arg>3s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:01:31.664336" elapsed="3.000378"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:34.665745" level="DEBUG">Test timeout 5 minutes 30 seconds active. 252.81803488731384 seconds left.</msg>
<arg>Step 11: Click</arg>
<arg>${IMAGE_DIR}/save-close-order.png</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:34.664714" elapsed="0.001031"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:34.665745" level="DEBUG">Test timeout 5 minutes 30 seconds active. 252.81803488731384 seconds left.</msg>
<msg time="2025-08-15T14:01:34.665745" level="INFO">${step11_start} = 2025-08-15 14:01:34.666</msg>
<var>${step11_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:34.665745" elapsed="0.000000"/>
</kw>
<kw name="Click" owner="Sikuli">
<msg time="2025-08-15T14:01:34.665745" level="DEBUG">Test timeout 5 minutes 30 seconds active. 252.81803488731384 seconds left.</msg>
<msg time="2025-08-15T14:01:35.880123" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262894987.png</msg>
<msg time="2025-08-15T14:01:35.880123" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262894987.png'/&gt;
[log] CLICK on L[1240,680]@S(0) (601 msec)</msg>
<arg>${IMAGE_DIR}/save-close-order.png</arg>
<doc>Click</doc>
<status status="PASS" start="2025-08-15T14:01:34.665745" elapsed="1.214378"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:35.880123" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.6036560535431 seconds left.</msg>
<msg time="2025-08-15T14:01:35.880123" level="INFO">${timestamp} = 20250815_140135</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:35.880123" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:35.880123" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.6036560535431 seconds left.</msg>
<msg time="2025-08-15T14:01:35.880123" level="INFO">${screenshot_name} = step_11_20250815_140135.png</msg>
<var>${screenshot_name}</var>
<arg>step_11_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:35.880123" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:35.880123" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.6036560535431 seconds left.</msg>
<msg time="2025-08-15T14:01:35.889974" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_11_20250815_140135.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:35.880123" elapsed="0.009851"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:01:35.889974" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.59380507469177 seconds left.</msg>
<msg time="2025-08-15T14:01:35.889974" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:01:35.889974" elapsed="0.000000"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:01:35.889974" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.59380507469177 seconds left.</msg>
<msg time="2025-08-15T14:01:36.049838" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262895970.png</msg>
<msg time="2025-08-15T14:01:36.049838" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262895970.png'/&gt;</msg>
<msg time="2025-08-15T14:01:36.049838" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262895970.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:01:35.889974" elapsed="0.159864"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:01:36.049838" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.4339416027069 seconds left.</msg>
<msg time="2025-08-15T14:01:36.089881" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262895970.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262895970.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_11_20250815_140135.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_11_20250815_140135.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:01:36.049838" elapsed="0.040043"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:36.089881" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.39389824867249 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:36.089881" elapsed="0.000000"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:36.089881" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.39389824867249 seconds left.</msg>
<msg time="2025-08-15T14:01:36.089881" level="INFO">${step11_end} = 2025-08-15 14:01:36.090</msg>
<var>${step11_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:36.089881" elapsed="0.000000"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:01:36.099891" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.38388776779175 seconds left.</msg>
<msg time="2025-08-15T14:01:36.099891" level="INFO">${step11_duration} = 1.424</msg>
<var>${step11_duration}</var>
<arg>${step11_end}</arg>
<arg>${step11_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:01:36.089881" elapsed="0.010010"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:36.099891" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.38388776779175 seconds left.</msg>
<arg>Step 11 completed in ${step11_duration}s</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:36.099891" elapsed="0.000000"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-15T14:01:36.099891" level="DEBUG">Test timeout 5 minutes 30 seconds active. 251.38388776779175 seconds left.</msg>
<msg time="2025-08-15T14:01:38.126117" level="INFO">Slept 2 seconds.</msg>
<arg>2s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-15T14:01:36.099891" elapsed="2.026226"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:38.166105" level="DEBUG">Test timeout 5 minutes 30 seconds active. 249.31767392158508 seconds left.</msg>
<arg>Step 12: Click</arg>
<arg>${IMAGE_DIR}/order-no2.png</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:38.156133" elapsed="0.009972"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:38.166105" level="DEBUG">Test timeout 5 minutes 30 seconds active. 249.31767392158508 seconds left.</msg>
<msg time="2025-08-15T14:01:38.166105" level="INFO">${step12_start} = 2025-08-15 14:01:38.166</msg>
<var>${step12_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:38.166105" elapsed="0.000000"/>
</kw>
<kw name="Click" owner="Sikuli">
<msg time="2025-08-15T14:01:38.166105" level="DEBUG">Test timeout 5 minutes 30 seconds active. 249.31767392158508 seconds left.</msg>
<msg time="2025-08-15T14:01:39.423292" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262898526.png</msg>
<msg time="2025-08-15T14:01:39.423292" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262898526.png'/&gt;
[log] CLICK on L[723,384]@S(0) (586 msec)</msg>
<arg>${IMAGE_DIR}/order-no2.png</arg>
<doc>Click</doc>
<status status="PASS" start="2025-08-15T14:01:38.166105" elapsed="1.257187"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:39.423292" level="DEBUG">Test timeout 5 minutes 30 seconds active. 248.0604875087738 seconds left.</msg>
<msg time="2025-08-15T14:01:39.423292" level="INFO">${timestamp} = 20250815_140139</msg>
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:39.423292" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:39.423292" level="DEBUG">Test timeout 5 minutes 30 seconds active. 248.0604875087738 seconds left.</msg>
<msg time="2025-08-15T14:01:39.423292" level="INFO">${screenshot_name} = step_12_20250815_140139.png</msg>
<var>${screenshot_name}</var>
<arg>step_12_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:39.423292" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<msg time="2025-08-15T14:01:39.423292" level="DEBUG">Test timeout 5 minutes 30 seconds active. 248.0604875087738 seconds left.</msg>
<msg time="2025-08-15T14:01:39.433319" level="INFO">${screenshot_path} = C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6/step_12_20250815_140139.png</msg>
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="PASS" start="2025-08-15T14:01:39.423292" elapsed="0.010027"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<msg time="2025-08-15T14:01:39.433319" level="DEBUG">Test timeout 5 minutes 30 seconds active. 248.05046010017395 seconds left.</msg>
<msg time="2025-08-15T14:01:39.433319" level="INFO" html="true">Directory '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6&lt;/a&gt;' already exists.</msg>
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="PASS" start="2025-08-15T14:01:39.433319" elapsed="0.000000"/>
</kw>
<kw name="Capture Screen" owner="Sikuli">
<msg time="2025-08-15T14:01:39.433319" level="DEBUG">Test timeout 5 minutes 30 seconds active. 248.05046010017395 seconds left.</msg>
<msg time="2025-08-15T14:01:39.593760" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262899513.png</msg>
<msg time="2025-08-15T14:01:39.593760" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755262899513.png'/&gt;</msg>
<msg time="2025-08-15T14:01:39.593760" level="INFO">${temp_screenshot} = C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262899513.png</msg>
<var>${temp_screenshot}</var>
<doc>Capture whole screen, file name is returned</doc>
<status status="PASS" start="2025-08-15T14:01:39.433319" elapsed="0.160441"/>
</kw>
<kw name="Copy File" owner="OperatingSystem">
<msg time="2025-08-15T14:01:39.593760" level="DEBUG">Test timeout 5 minutes 30 seconds active. 247.89001965522766 seconds left.</msg>
<msg time="2025-08-15T14:01:39.623918" level="INFO" html="true">Copied file from '&lt;a href="file://C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262899513.png"&gt;C:\Users\UK-PC\AppData\Local\Temp\tmpnrj818mm\sikuli_captured\sikuliximage-1755262899513.png&lt;/a&gt;' to '&lt;a href="file://C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_12_20250815_140139.png"&gt;C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\screenshots\ae1160cf-8b3f-40c7-b81d-be34e05c55c6\step_12_20250815_140139.png&lt;/a&gt;'.</msg>
<arg>${temp_screenshot}</arg>
<arg>${screenshot_path}</arg>
<doc>Copies the source file into the destination.</doc>
<status status="PASS" start="2025-08-15T14:01:39.593760" elapsed="0.030158"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-15T14:01:39.623918" level="DEBUG">Test timeout 5 minutes 30 seconds active. 247.85986161231995 seconds left.</msg>
<arg>Screenshot saved: ${screenshot_path}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-15T14:01:39.623918" elapsed="0.000000"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-15T14:01:39.623918" level="DEBUG">Test timeout 5 minutes 30 seconds active. 247.85986161231995 seconds left.</msg>
<msg time="2025-08-15T14:01:39.623918" level="INFO">${step12_end} = 2025-08-15 14:01:39.624</msg>
<var>${step12_end}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-15T14:01:39.623918" elapsed="0.009520"/>
</kw>
<kw name="Subtract Date From Date" owner="DateTime">
<msg time="2025-08-15T14:01:39.633438" level="DEBUG">Test timeout 5 minutes 30 seconds active. 247.85034084320068 seconds left.</msg>
<msg time="2025-08-15T14:01:39.633438" level="INFO">${step12_duration} = 1.458</msg>
<var>${step12_duration}</var>
<arg>${step12_end}</arg>
<arg>${step12_start}</arg>
<doc>Subtracts date from another date and returns time between.</doc>
<status status="PASS" start="2025-08-15T14:01:39.633438" elapsed="0.000000"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
