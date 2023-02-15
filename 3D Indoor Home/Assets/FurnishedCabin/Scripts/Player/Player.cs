using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour {
    public CameraScript snapCam;

    void Update()
    {
        snapCam.CallTakeSnapshot();
    }
}