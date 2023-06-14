# Python Robotics Sandbox
I always liked the idea of stuff moving around in relation to other stuff so robotics and game development with Unity or Unreal engine and the whole concept of representing objects through transforms.
A visualization for Inverse Kinematics with Python


# Notes

https://robotics.stackexchange.com/questions/8621/forward-kinematic-computing-the-transformation-matrix

https://robotics-explained.com/inversekinematics

Ok, getting VTK to work was the most painful process ever I swear.

- Plotly uses a XZY coordinate system where Z is upwards and XY is the horizontal plane.
- However, VTK uses a XZY coordinate system, similar to Unity and other 3D engines.

Since I've been working with plotly this whole time there were quite a few issues in converting from one coordinate system to the other.

Before figuring out the issues I had to fix some bugs though...
## 1. Correct Rotation order
Even though I KNEW that matrix multiplication is not commutative, for some reason I forgot about it and I was calculating the Transform's rotation matrix as `Rx @ Ry @ Rz` instead of the correct way which should be `Rz @ Ry @ Rx` for a total rotation in the order `X -> Y -> Z`.
This actually caused a gimbal lock where the rotation on the x axis would "not work" anymore when the object was turned perpendicularly

## 2. Correct re-conversion rotation order
Once that was solved, there was still the issue on how to pass the orientation to the VTK actor in the correct way.
From the official [VTK documentation](https://vtk.org/doc/release/5.0/html/a01919.html) we can see that the orientation property of an actor expects a rotation in the order `Rot(y) Rot(x) Rot (z)`.

Now, rotation matrices represent the orientation of an object in space like a quaternion does, and the order does not matter. This means that once we represent everything in a mnatricial form, we can revert it to a different representation that uses whichever angle order we want.

BUT, this is not as easy as it sounds. Converting from Rotation Matrices or quaternions to angles actually has a big issue: Singularities.
To make sure this was all correct I double checked everything with an [online 3D rotation covnerter](https://www.andre-gaschler.com/rotationconverter/) as well as a little project in Unity3D to double check the transforms and rotations

This is the Unity script I attached to each joint:

```CS
[ExecuteInEditMode]
public class getAbsRotation : MonoBehaviour
{
    [TextArea(3,100)]
    public string ret = "";
    void Update()
    {
        ret = this.name +":\n";
        var t = this.transform;
        var local_matrix = Matrix4x4.TRS(t.localPosition, t.localRotation, t.localScale);
        var abs_matrix = Matrix4x4.TRS(t.position, t.rotation, t.localScale);
        ret += "\nLocal Trans Matrix:\n" + local_matrix;
        ret += "\nLocal Position: " + t.localPosition;
        ret += "\nLocal Euler Angles: " + t.localEulerAngles;
        ret += "\nLocal Rotation: " + t.localRotation;

        ret += "\n\nAbsolute Trans Matrix:\n" + abs_matrix;
        ret += "\nAbsolute Position: " + t.position;
        ret += "\nAbsolute Euler Angles: " + t.eulerAngles;
        ret += "\nAbsolute Rotation: " + t.rotation;
        Debug.Log(ret);
    }
}
```

I obviously replicated the same transform hierarchy by matching the offsets, parent-child relationships and angles.

All of this really helped to figure out what was wrong.

The online converted actually uses `THREE.js` built-in functions so I delved into THREE.js code to find the conversion function and sure thing I found it! (`Euler.js`)[https://github.com/mrdoob/three.js/blob/dev/src/math/Euler.js#L105].

As it is obvious from that function, the order in which we convert the rotation matrix to angles matters.

It matters for two reasons:
1. We need to (check for singularities)[http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/] before converting the angles 
2. We need to match the order in which we decompose the matrix and the order in which we re-apply the angles. So if we extract the angles in the order ZYX then we need to re-apply them as XYZ.

So I finally re-wrote the function to go from rotation matrices to euler angles as such:

```python
  def get_euler_angles(transform, order="xyz"):
    matrix = transform.mat[0:3, 0:3]
    matrix = np.array(matrix)
    m11, m12, m13 = matrix[0]
    m21, m22, m23 = matrix[1]
    m31, m32, m33 = matrix[2]
    
    if order == "xyz":
      y = math.asin(np.clip(m13, -1, 1))
      # Checks for gymbal lock
      if abs(m13) < 0.999:
        x = math.atan2(-m23, m33)
        z = math.atan2(-m12, m11)
      else:
        x = math.atans(m32, m22)
        z = 0
    elif order == "yxz":
      x = math.asin(-np.clip(m23, -1, 1))
      # Checks for gymbal lock
      if abs(m23) < 0.999:
        y = math.atan2(m13, m33)
        z = math.atan2(m21, m22)
      else:
        y = math.atan2(-m31, m11)
        z = 0
    elif order == "zxy": # use this one to re-obtain the rotation angles after applying them to plotly
      x = math.asin(np.clip(m32, -1, 1))
      # Checks for gymbal lock
      if abs(m32) < 0.999:
        y = math.atan2(-m31, m33)
        z = math.atan2(-m12, m22)
      else:
        y = 0
        z = math.atan2(m21, m11)
    elif order == "zyx": # use this one before passing the orientation to VTK actors
      y = math.asin(-np.clip(m31, -1, 1))
      # Checks for gymbal lock
      if abs(m31) < 0.999:
        x = math.atan2(m32, m33)
        z = math.atan2(m21, m11)
      else:
        x = 0
        z = math.atan2(-m12, m22)
      
    x = math.degrees(x)
    y = math.degrees(y)
    z = math.degrees(z)
    return [x, y, z]
```

It actually took me a little bit and some trial and error to figure out the right order.
In fact, even if you applied the rotation as `XYZ` and then extract it as `XYZ` it won't work as you should use `ZYX` to retrieve it back. Not only that but if you retrieve it as say `ZYX`, you CANNOT use these angles to rotate an object with the order `YXZ`, you need to instead retrieve the angles as `ZXY` and then use them as `YXZ`.

So in short:
- Once you apply a rotation to an object in Plotly using the order `XYZ` you can then re-obtain that rotation by converting the rotation matrix to angles using the order `ZYX`. so `Apply Euler Angles in XYZ -> Rotation Matrix -> Retrieve Euler Angles in XYZ -> Apply Euler Angles in XYZ...`
- To go from rotation matrix to VTK actor orientation you should first retrieve the euler angles from the rotation matrix as `ZXY` and then pass them to VTK which expects a rotation in the order `YXZ`. So: `Apply Euler Angles in XYZ -> Rotation Matrix -> Retrieve Euler Angles in ZXY -> Pass VTK orientation with Euler Angles in YXZ...`

There are still some issues with certain rotations e.g. X=90, Y=90, Z=90 but overall now it works as it should.
In fact, before fixing these bugs, after rotating a joint on its X and Y axis and then trying to rotate it around its Z axis, the joint would "spin around" itself which is actually incorrect, if there have been rotations on X and Y it should rotate accordingly independently of its orientation.