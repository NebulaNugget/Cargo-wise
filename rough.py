<?xml version="1.0" encoding="UTF-8"?>
<robot generator="Robot 7.3 (Python 3.11.0 on win32)" generated="2025-08-19T19:22:21.361655" rpa="false" schemaversion="5">
<suite id="s1" name="Tmpo9 Vjza" source="C:\Users\UK-PC\AppData\Local\Temp\tmpo9_vjza_.robot">
<test id="s1-t1" name="Execute Sikuli Task" line="15">
<kw name="Initialize Sikuli Environment" type="SETUP">
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-19T19:22:28.679759" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.9929702281952 seconds left.</msg>
<msg time="2025-08-19T19:22:28.681768" level="INFO">Initializing Sikuli environment</msg>
<arg>Initializing Sikuli environment</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-19T19:22:28.677758" elapsed="0.004010"/>
</kw>
<kw name="Set Library Search Order" owner="BuiltIn">
<msg time="2025-08-19T19:22:28.682762" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.9899673461914 seconds left.</msg>
<arg>Sikuli</arg>
<doc>Sets the resolution order to use when a name matches multiple keywords.</doc>
<status status="PASS" start="2025-08-19T19:22:28.682762" elapsed="0.000996"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-19T19:22:28.684767" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.98796224594116 seconds left.</msg>
<arg>Starting Sikuli Process...</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-19T19:22:28.684767" elapsed="0.000992"/>
</kw>
<kw name="Start Sikuli Process" owner="Sikuli">
<msg time="2025-08-19T19:22:28.686766" level="DEBUG">Test timeout 5 minutes 30 seconds active. 329.9859628677368 seconds left.</msg>
<msg time="2025-08-19T19:22:28.689804" level="DEBUG">Free TCP port is: 55653</msg>
<msg time="2025-08-19T19:22:28.692778" level="INFO">Starting process:
java -jar "C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\venv\Lib\site-packages\SikuliLibrary\lib\SikuliLibrary.jar" 55653 C:\Users\UK-PC\AppData\Local\Temp\tmpcy97yscd</msg>
<msg time="2025-08-19T19:22:28.692778" level="DEBUG">Process configuration:
cwd:     C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend
shell:   True
stdout:  C:\Users\UK-PC\AppData\Local\Temp\tmpcy97yscd\Sikuli_java_stdout_1755627748.690793.txt
stderr:  C:\Users\UK-PC\AppData\Local\Temp\tmpcy97yscd\Sikuli_java_stderr_1755627748.690793.txt
stdin:   None
alias:   None
env:     None</msg>
<msg time="2025-08-19T19:22:28.710777" level="INFO">Start sikuli java process on port 55653</msg>
<msg time="2025-08-19T19:22:31.901076" level="INFO">Sikuli java process is started</msg>
<status status="PASS" start="2025-08-19T19:22:28.686766" elapsed="7.369550"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-19T19:22:36.058324" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.6144049167633 seconds left.</msg>
<arg>Adding image path: ${IMAGE_DIR}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-19T19:22:36.057324" elapsed="0.002985"/>
</kw>
<kw name="Add Image Path" owner="Sikuli">
<msg time="2025-08-19T19:22:36.061324" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.61140513420105 seconds left.</msg>
<arg>${IMAGE_DIR}</arg>
<doc>Add image path</doc>
<status status="PASS" start="2025-08-19T19:22:36.060309" elapsed="0.103000"/>
</kw>
<kw name="Set Move Mouse Delay" owner="Sikuli">
<msg time="2025-08-19T19:22:36.164322" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.50840640068054 seconds left.</msg>
<arg>0.5</arg>
<doc>Set move mouse delay</doc>
<status status="PASS" start="2025-08-19T19:22:36.164322" elapsed="0.032013"/>
</kw>
<kw name="Set Min Similarity" owner="Sikuli">
<msg time="2025-08-19T19:22:36.197420" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.4753084182739 seconds left.</msg>
<arg>0.5</arg>
<doc>Set min similarity (accuracy of matching elements).</doc>
<status status="PASS" start="2025-08-19T19:22:36.197420" elapsed="0.016903"/>
</kw>
<kw name="Run Keyword If" owner="BuiltIn">
<kw name="Launch CargoWise Application">
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-19T19:22:36.221356" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.45137333869934 seconds left.</msg>
<msg time="2025-08-19T19:22:36.223305" level="INFO">Launching application from: C:\Program Files (x86)\WiseTech Global\WiseCloud Client\WiseCloudClient.exe</msg>
<arg>Launching application from: ${APP_PATH}</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-19T19:22:36.219373" elapsed="0.004948"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-19T19:22:36.225327" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.4474015235901 seconds left.</msg>
<arg>Launching application: ${APP_PATH}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-19T19:22:36.224321" elapsed="0.002989"/>
</kw>
<kw name="Start Process" owner="Process">
<msg time="2025-08-19T19:22:36.228334" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.4443943500519 seconds left.</msg>
<msg time="2025-08-19T19:22:36.229330" level="INFO">Starting process:
C:\Program Files (x86)\WiseTech Global\WiseCloud Client\WiseCloudClient.exe</msg>
<msg time="2025-08-19T19:22:36.229330" level="DEBUG">Process configuration:
cwd:     C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend
shell:   True
stdout:  PIPE
stderr:  PIPE
stdin:   None
alias:   None
env:     None</msg>
<msg time="2025-08-19T19:22:36.245307" level="INFO">${process} = &lt;Popen: returncode: None args: 'C:\\Program Files (x86)\\WiseTech Global\\Wi...&gt;</msg>
<var>${process}</var>
<arg>${APP_PATH}</arg>
<arg>shell=True</arg>
<doc>Starts a new process on background.</doc>
<status status="PASS" start="2025-08-19T19:22:36.227310" elapsed="0.017997"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-19T19:22:36.246308" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.42642068862915 seconds left.</msg>
<msg time="2025-08-19T19:22:36.247314" level="INFO">${timestamp} = 2025-08-19 19:22:36.246</msg>
<var>${timestamp}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-19T19:22:36.245307" elapsed="0.002007"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-19T19:22:36.248321" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.4244079589844 seconds left.</msg>
<arg>Application launch initiated at ${timestamp}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-19T19:22:36.247314" elapsed="0.003002"/>
</kw>
<kw name="Sleep" owner="BuiltIn">
<msg time="2025-08-19T19:22:36.251327" level="DEBUG">Test timeout 5 minutes 30 seconds active. 322.42140221595764 seconds left.</msg>
<msg time="2025-08-19T19:22:51.253673" level="INFO">Slept 15 seconds.</msg>
<arg>15s</arg>
<doc>Pauses the test executed for the given time.</doc>
<status status="PASS" start="2025-08-19T19:22:36.250316" elapsed="15.003357"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-19T19:22:51.255530" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.41719937324524 seconds left.</msg>
<arg>Application should be started now</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-19T19:22:51.254520" elapsed="0.002002"/>
</kw>
<doc>Launch the CargoWise application</doc>
<status status="PASS" start="2025-08-19T19:22:36.217326" elapsed="15.040219"/>
</kw>
<arg>'${APP_PATH}' != '${EMPTY}'</arg>
<arg>Launch CargoWise Application</arg>
<doc>Runs the given keyword with the given arguments, if ``condition`` is true.</doc>
<status status="PASS" start="2025-08-19T19:22:36.214323" elapsed="15.043222"/>
</kw>
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-19T19:22:51.258538" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.4141912460327 seconds left.</msg>
<msg time="2025-08-19T19:22:51.260534" level="INFO">Sikuli environment initialized</msg>
<arg>Sikuli environment initialized</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-19T19:22:51.258538" elapsed="0.001996"/>
</kw>
<doc>Initialize Sikuli with minimal settings</doc>
<status status="PASS" start="2025-08-19T19:22:28.674907" elapsed="22.585627"/>
</kw>
<kw name="Run Keyword And Continue On Failure" owner="BuiltIn">
<kw name="Execute Task With Progress Logging">
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-19T19:22:51.265521" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.4072072505951 seconds left.</msg>
<msg time="2025-08-19T19:22:51.267522" level="INFO">${start_time} = 2025-08-19 19:22:51.267</msg>
<var>${start_time}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-19T19:22:51.264525" elapsed="0.002997"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-19T19:22:51.268523" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.4042057991028 seconds left.</msg>
<arg>Task execution started at ${start_time}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-19T19:22:51.267522" elapsed="0.001993"/>
</kw>
<kw name="Run Keyword And Return Status" owner="BuiltIn">
<kw name="Run Keyword With Timeout">
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-19T19:22:51.272524" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.40020513534546 seconds left.</msg>
<arg>Running keyword with timeout: ${keyword} (${timeout})</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-19T19:22:51.271522" elapsed="0.001996"/>
</kw>
<kw name="Run Keyword And Return Status" owner="BuiltIn">
<kw name="Wait Until Keyword Succeeds" owner="BuiltIn">
<kw name="Run Sikuli Task">
<kw name="Log" owner="BuiltIn">
<msg time="2025-08-19T19:22:51.280528" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.39220118522644 seconds left.</msg>
<msg time="2025-08-19T19:22:51.281517" level="INFO">Starting Sikuli task execution</msg>
<arg>Starting Sikuli task execution</arg>
<doc>Logs the given message with the given level.</doc>
<status status="PASS" start="2025-08-19T19:22:51.280528" elapsed="0.000989"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-19T19:22:51.282520" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.39020895957947 seconds left.</msg>
<arg>Executing Sikuli task...</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-19T19:22:51.282520" elapsed="0.001995"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-19T19:22:51.285526" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.38720321655273 seconds left.</msg>
<msg time="2025-08-19T19:22:51.286518" level="INFO">${task_start} = 2025-08-19 19:22:51.287</msg>
<var>${task_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-19T19:22:51.284515" elapsed="0.002003"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-19T19:22:51.287522" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.38520646095276 seconds left.</msg>
<arg>Task started at ${task_start}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-19T19:22:51.287522" elapsed="0.000994"/>
</kw>
<kw name="Log To Console" owner="BuiltIn">
<msg time="2025-08-19T19:22:51.290534" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.38219475746155 seconds left.</msg>
<arg>Step 1: Input Text</arg>
<arg>${IMAGE_DIR}/order-buyer.png</arg>
<arg>${BUYER}</arg>
<doc>Logs the given message to the console.</doc>
<status status="PASS" start="2025-08-19T19:22:51.289524" elapsed="0.001991"/>
</kw>
<kw name="Get Current Date" owner="DateTime">
<msg time="2025-08-19T19:22:51.291515" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.3812139034271 seconds left.</msg>
<msg time="2025-08-19T19:22:51.293523" level="INFO">${step1_start} = 2025-08-19 19:22:51.293</msg>
<var>${step1_start}</var>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="PASS" start="2025-08-19T19:22:51.291515" elapsed="0.002008"/>
</kw>
<kw name="Input Text" owner="Sikuli">
<msg time="2025-08-19T19:22:51.295535" level="DEBUG">Test timeout 5 minutes 30 seconds active. 307.3771939277649 seconds left.</msg>
<msg time="2025-08-19T19:22:55.667119" level="INFO">Input Text:
luclenliv</msg>
<msg time="2025-08-19T19:22:55.667119" level="DEBUG">Saved path: C:\Users\UK-PC\AppData\Local\Temp\tmpcy97yscd\sikuli_captured\sikuliximage-1755627775465.png</msg>
<msg time="2025-08-19T19:22:55.667119" level="INFO" html="true">&lt;img src='sikuli_captured/sikuliximage-1755627775465.png'/&gt;</msg>
<msg time="2025-08-19T19:22:55.667119" level="FAIL">com.github.rainmanwy.robotframework.sikulilib.exceptions.TimeoutException: Timeout happened, could not find P(C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\cargowise_images/order-buyer.png) S: 0.5</msg>
<msg time="2025-08-19T19:22:55.668112" level="DEBUG">com.github.rainmanwy.robotframework.sikulilib.exceptions.TimeoutException: Timeout happened, could not find P(C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\cargowise_images/order-buyer.png) S: 0.5
	at com.github.rainmanwy.robotframework.sikulilib.keywords.ScreenKeywords.wait(ScreenKeywords.java:329)
	at com.github.rainmanwy.robotframework.sikulilib.keywords.ScreenKeywords.click(ScreenKeywords.java:136)
	at com.github.rainmanwy.robotframework.sikulilib.keywords.ScreenKeywords.inputText(ScreenKeywords.java:395)
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104)
	at java.base/java.lang.reflect.Method.invoke(Method.java:565)
	at org.robotframework.javalib.reflection.KeywordInvoker.invoke(KeywordInvoker.java:63)
	at org.robotframework.javalib.beans.annotation.AnnotationKeywordExtractor$1.execute(AnnotationKeywordExtractor.java:66)
	at org.robotframework.javalib.library.KeywordFactoryBasedLibrary.runKeyword(KeywordFactoryBasedLibrary.java:40)
	at org.robotframework.javalib.library.AnnotationLibrary.runKeyword(AnnotationLibrary.java:129)
	at com.github.rainmanwy.robotframework.sikulilib.SikuliLibrary.runKeyword(SikuliLibrary.java:42)
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104)
	at java.base/java.lang.reflect.Method.invoke(Method.java:565)
	at org.robotframework.remoteserver.library.DynamicApiRemoteLibrary.runKeyword(DynamicApiRemoteLibrary.java:70)
	at org.robotframework.remoteserver.servlet.ServerMethods.run_keyword(ServerMethods.java:86)
	at org.robotframework.remoteserver.servlet.ServerMethods.run_keyword(ServerMethods.java:148)
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104)
	at java.base/java.lang.reflect.Method.invoke(Method.java:565)
	at org.apache.xmlrpc.server.ReflectiveXmlRpcHandler.invoke(ReflectiveXmlRpcHandler.java:115)
	at org.apache.xmlrpc.server.ReflectiveXmlRpcHandler.execute(ReflectiveXmlRpcHandler.java:106)
	at org.apache.xmlrpc.server.XmlRpcServerWorker.execute(XmlRpcServerWorker.java:46)
	at org.apache.xmlrpc.server.XmlRpcServer.execute(XmlRpcServer.java:86)
	at org.apache.xmlrpc.server.XmlRpcStreamServer.execute(XmlRpcStreamServer.java:200)
	at org.apache.xmlrpc.webserver.XmlRpcServletServer.execute(XmlRpcServletServer.java:112)
	at org.apache.xmlrpc.webserver.XmlRpcServlet.doPost(XmlRpcServlet.java:196)
	at org.robotframework.remoteserver.servlet.RemoteServerServlet.doPost(RemoteServerServlet.java:122)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:707)
	at org.robotframework.remoteserver.servlet.RemoteServerServlet.service(RemoteServerServlet.java:102)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:790)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:763)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:569)
	at org.eclipse.jetty.server.handler.ScopedHandler.nextHandle(ScopedHandler.java:233)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1377)
	at org.eclipse.jetty.server.handler.ScopedHandler.nextScope(ScopedHandler.java:188)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:507)
	at org.eclipse.jetty.server.handler.ScopedHandler.nextScope(ScopedHandler.java:186)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1292)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:141)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:127)
	at org.eclipse.jetty.server.Server.handle(Server.java:501)
	at org.eclipse.jetty.server.HttpChannel.lambda$handle$1(HttpChannel.java:383)
	at org.eclipse.jetty.server.HttpChannel.dispatch(HttpChannel.java:556)
	at org.eclipse.jetty.server.HttpChannel.handle(HttpChannel.java:375)
	at org.eclipse.jetty.server.HttpConnection.onFillable(HttpConnection.java:273)
	at org.eclipse.jetty.io.AbstractConnection$ReadCallback.succeeded(AbstractConnection.java:311)
	at org.eclipse.jetty.io.FillInterest.fillable(FillInterest.java:105)
	at org.eclipse.jetty.io.ChannelEndPoint$1.run(ChannelEndPoint.java:104)
	at org.eclipse.jetty.util.thread.strategy.EatWhatYouKill.runTask(EatWhatYouKill.java:336)
	at org.eclipse.jetty.util.thread.strategy.EatWhatYouKill.doProduce(EatWhatYouKill.java:313)
	at org.eclipse.jetty.util.thread.strategy.EatWhatYouKill.tryProduce(EatWhatYouKill.java:171)
	at org.eclipse.jetty.util.thread.strategy.EatWhatYouKill.run(EatWhatYouKill.java:129)
	at org.eclipse.jetty.util.thread.ReservedThreadExecutor$ReservedThread.run(ReservedThreadExecutor.java:375)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:806)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$Runner.run(QueuedThreadPool.java:938)
	at java.base/java.lang.Thread.run(Thread.java:1447)
Caused by: FindFailed: C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\cargowise_images/order-buyer.png: (87x45) in R[0,0 1366x768]@S(0)
  Line 2222, in file Region.java

	at org.sikuli.script.Region.wait(Region.java:2222)
	at com.github.rainmanwy.robotframework.sikulilib.keywords.ScreenKeywords.wait(ScreenKeywords.java:323)
	... 53 more
</msg>
<arg>${IMAGE_DIR}/order-buyer.png</arg>
<arg>${BUYER}</arg>
<doc>Input text.
 Image could be empty</doc>
<status status="FAIL" start="2025-08-19T19:22:51.294543" elapsed="4.373569">com.github.rainmanwy.robotframework.sikulilib.exceptions.TimeoutException: Timeout happened, could not find P(C:\Users\UK-PC\Desktop\AI driven cargo-wise automation framework\cargowise-ai-backend\cargowise_images/order-buyer.png) S: 0.5</status>
</kw>
<kw name="Get Current Date" owner="DateTime">
<var>${timestamp}</var>
<arg>result_format=%Y%m%d_%H%M%S</arg>
<doc>Returns current local or UTC time with an optional increment.</doc>
<status status="NOT RUN" start="2025-08-19T19:22:55.669123" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<var>${screenshot_name}</var>
<arg>step_1_${timestamp}.png</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="NOT RUN" start="2025-08-19T19:22:55.669123" elapsed="0.000000"/>
</kw>
<kw name="Set Variable" owner="BuiltIn">
<var>${screenshot_path}</var>
<arg>${SCREENSHOT_DIR}/${screenshot_name}</arg>
<doc>Returns the given values which can then be assigned to a variables.</doc>
<status status="NOT RUN" start="2025-08-19T19:22:55.669123" elapsed="0.000000"/>
</kw>
<kw name="Create Directory" owner="OperatingSystem">
<arg>${SCREENSHOT_DIR}</arg>
<doc>Creates the specified directory.</doc>
<status status="NOT RUN" start="2025-08-19T19:22:55.669123" elapsed="0.000000"/>
</kw>