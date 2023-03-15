Working with humanoid characters requires specific features in Unity's Animation System. Due to the prevalence of humanoid figures in video games, Unity offers a specific process and a larger toolkit for humanoid animations.
Unity uses the Avatar system to determine which animation models are humanoid in design and which portions of the models represent the legs, arms, head, and body. Because multiple humanoid characters have comparable bone structures, it is easy to translate animations from one to another, allowing retargeting and inverse kinematics (IK).

## Creating Humanoid
You can select the type of rig a model file (FBX, COLLADA, etc.) is on the Rig tab of the Model Importer settings after it has been imported.

Click Apply after selecting Humanoid for a Humanoid rig. Your current bone structure will be compared to the Avatar's bone structure by Mecanim. By examining the relationships between the bones in the rig, it can frequently perform this task automatically.

You will notice a check mark next to the Customize menu if the match was successful.

![alt text](https://docs.unity3d.com/550/Documentation/uploads/Main/MecanimImporterRigTab.png)

Also, in the case of a successful match, an Avatar sub-asset is added to the model asset, which you will be able to see in the project view hierarchy.

![alt text](https://docs.unity3d.com/550/Documentation/uploads/Main/MecanimFBXNoAvatar.png)

Selecting the avatar sub-asset will bring up the inspector. You can then configure the avatar.

![alt text](https://docs.unity3d.com/550/Documentation/uploads/Main/MecanimAvatarCreated.png)

If Mecanim was unable to create the Avatar, you will see a cross next to the Configure button, and no Avatar sub-asset will be added. When this happens, you need to configure the avatar manually.

## Configuration of the Avatar

Since the Avatar is such an important aspect of the Mecanim system, it is important that it is configured properly for your model. So, whether the automatic Avatar creation fails or succeeds, you need to go into the Configure Avatar mode to ensure your Avatar is valid and properly set up. It is important that your character’s bone structure matches Mecanim’s predefined bone structure and that the model is in T-pose.

If the automatic Avatar creation fails, you will see a cross next to the Configure button.

![alt text](https://docs.unity3d.com/550/Documentation/uploads/Main/MecanimAvatarInvalid.png)

If it succeeds, you will see a check/tick mark:

![alt text](https://docs.unity3d.com/550/Documentation/uploads/Main/MecanimAvatarApplied.png)

Here, success simply means all of the required bones have been matched but for better results, you might want to match the optional bones as well and get the model into a proper T-pose.

When you go to the Configure … menu, the editor will ask you to save your scene. The reason for this is that in Configure mode, the Scene View is used to display bone, muscle and animation information for the selected model alone, without displaying the rest of the scene.

![alt text](https://docs.unity3d.com/550/Documentation/uploads/Main/MecanimConfigureAvatarSaveDialog.png)

Please follow this video tutorial on Youtube: https://www.youtube.com/watch?v=pbaOGZzth6g
