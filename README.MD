#Auto Checker
Auto-Checker is a python script which is used for auto-checking whether minecraft mod(s) has specific keywords in its code or specific extensions(such like .bat) in its jar file.

##How to use it?
**Step 0:** Auto-checker is written in python3, so you need to install python3 before you use it. You should also download or clone this repository for preparation.  
**Step 1:** Put the mod you want to check in the "input" folder.   
**Step 2:** Modify the .cfg files in "config" folder to your preference.  
**Step 3:** Run the "Auto_Checker.py" script in a python shell and then check out the log information in the shell. The same log information will be saved in the "logs" folder.  

##How to modify the config
Basically, there is three configs in the "config" folder and they will be automatically generated if they do not exist.   

For the "warning_extensions.cfg", you should add the extensions which you consider a latent malware will have. For instance, ".bat" and ".exe" should not exist in a Minecraft mod's jar file, so we should add them in this config.  

For the "warning_keywords.cfg", you should add the keywords which malicious codes would have. For instance, we can add "GameType.CREATIVE" in this config, since this field may become very dangerous if someone use it in a mod to change the players from survival mode into creative mode when they play on a server.  
 
For the "checkmode.cfg", you should add the extensions which the files that you want to check have. For instance, we can add ".java,.scala" in the config and set the check mode to "white namelist"(this is also the default setting) so that Auto-Checker will check the .java and .scala files to find out whether these files contain the keywords in "warning_keywords.cfg".

##License
The FernFlower-2.0-SNAPSHOT.jar is built from [its code](https://github.com/MinecraftForge/FernFlower) so its license is its original license - [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0).
The license of the other stuffs in this repository is MIT.  
