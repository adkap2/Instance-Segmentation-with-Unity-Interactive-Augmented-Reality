Working with humanoid characters requires specific features in Unity's Animation System. Due to the prevalence of humanoid figures in video games, Unity offers a specific process and a larger toolkit for humanoid animations.
Unity uses the Avatar system to determine which animation models are humanoid in design and which portions of the models represent the legs, arms, head, and body. Because multiple humanoid characters have comparable bone structures, it is easy to translate animations from one to another, allowing retargeting and inverse kinematics (IK).

##Creating Humanoid
You can select the type of rig a model file (FBX, COLLADA, etc.) is on the Rig tab of the Model Importer settings after it has been imported.

Click Apply after selecting Humanoid for a Humanoid rig. Your current bone structure will be compared to the Avatar's bone structure by Mecanim. By examining the relationships between the bones in the rig, it can frequently perform this task automatically.

You will notice a check mark next to the Customize menu if the match was successful.

![alt text](https://docs.unity3d.com/550/Documentation/uploads/Main/MecanimImporterRigTab.png)

