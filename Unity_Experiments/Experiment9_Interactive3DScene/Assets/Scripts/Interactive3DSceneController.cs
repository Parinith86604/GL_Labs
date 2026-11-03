
using UnityEngine;
using System.Collections.Generic;

public class Interactive3DSceneController : MonoBehaviour
{
    // ==========================================
    // OBJECTS AND ORIGINAL TRANSFORMS
    // ==========================================

    private readonly List<GameObject> objects =
        new List<GameObject>();

    private readonly List<Vector3> initialPositions =
        new List<Vector3>();

    private readonly List<Vector3> initialScales =
        new List<Vector3>();

    private readonly List<Quaternion> initialRotations =
        new List<Quaternion>();

    private readonly List<Mesh> generatedMeshes =
        new List<Mesh>();

    private int selectedIndex = 0;

    private Vector2 menuScrollPosition = Vector2.zero;

    // ==========================================
    // MATERIALS
    // ==========================================

    private Material blackMaterial;
    private Material blueMaterial;
    private Material roseMaterial;

    // ==========================================
    // CAMERA SETTINGS
    // ==========================================

    private Camera sceneCamera;

    private Vector3 cameraTarget =
        new Vector3(0f, 0.8f, 0f);

    private float cameraYaw = -36f;
    private float cameraPitch = 25f;
    private float cameraDistance = 15f;

    private const float CameraRotateSpeed = 100f;
    private const float CameraZoomSpeed = 8f;

    // ==========================================
    // START
    // ==========================================

    private void Start()
    {
        CreateMaterials();
        SetupCamera();
        SetupLighting();
        CreateEnvironment();
        Create3DObjects();
        SaveInitialTransforms();

        Debug.Log("Experiment 9 scene created successfully.");
    }

    // ==========================================
    // MATERIAL CREATION
    // ==========================================

    private Material CreateMaterial(Color color)
    {
        Shader shader = Shader.Find(
            "Universal Render Pipeline/Lit"
        );

        if (shader == null)
        {
            shader = Shader.Find(
                "Universal Render Pipeline/Simple Lit"
            );
        }

        if (shader == null)
        {
            shader = Shader.Find("Standard");
        }

        if (shader == null)
        {
            Debug.LogError("Material shader not found.");
            return null;
        }

        Material material = new Material(shader);
        material.color = color;

        if (material.HasProperty("_Smoothness"))
            material.SetFloat("_Smoothness", 0.3f);

        if (material.HasProperty("_Metallic"))
            material.SetFloat("_Metallic", 0.1f);

        return material;
    }

    private void CreateMaterials()
    {
        // JET BLACK
        blackMaterial = CreateMaterial(
            new Color(0.025f, 0.025f, 0.04f)
        );

        // CERULEAN BLUE
        blueMaterial = CreateMaterial(
            new Color(0f, 0.48f, 0.65f)
        );

        // NEON ROSE
        roseMaterial = CreateMaterial(
            new Color(1f, 0.08f, 0.45f)
        );
    }

    // ==========================================
    // CAMERA SETUP
    // ==========================================

    private void SetupCamera()
    {
        sceneCamera = Camera.main;

        if (sceneCamera == null)
        {
            GameObject cameraObject =
                new GameObject("Main Camera");

            cameraObject.tag = "MainCamera";

            sceneCamera =
                cameraObject.AddComponent<Camera>();
        }

        sceneCamera.fieldOfView = 55f;
        sceneCamera.nearClipPlane = 0.1f;
        sceneCamera.farClipPlane = 100f;

        sceneCamera.clearFlags =
            CameraClearFlags.SolidColor;

        sceneCamera.backgroundColor =
            new Color(0.025f, 0.035f, 0.08f);

        sceneCamera.allowHDR = true;
        sceneCamera.allowMSAA = true;

        UpdateCameraOrbit();
    }

    private void UpdateCameraOrbit()
    {
        if (sceneCamera == null)
            return;

        Quaternion rotation = Quaternion.Euler(
            cameraPitch,
            cameraYaw,
            0f
        );

        Vector3 offset = rotation *
            new Vector3(0f, 0f, -cameraDistance);

        sceneCamera.transform.position =
            cameraTarget + offset;

        sceneCamera.transform.rotation = rotation;
    }

    // ==========================================
    // LAPTOP KEYBOARD CAMERA CONTROLS
    // ==========================================

    private void HandleCameraControls()
    {
        float rotateSpeed =
            CameraRotateSpeed * Time.deltaTime;

        float zoomSpeed =
            CameraZoomSpeed * Time.deltaTime;

        bool cameraChanged = false;

        // Rotate left
        if (Input.GetKey(KeyCode.A) ||
            Input.GetKey(KeyCode.LeftArrow))
        {
            cameraYaw -= rotateSpeed;
            cameraChanged = true;
        }

        // Rotate right
        if (Input.GetKey(KeyCode.D) ||
            Input.GetKey(KeyCode.RightArrow))
        {
            cameraYaw += rotateSpeed;
            cameraChanged = true;
        }

        // Look upward
        if (Input.GetKey(KeyCode.W) ||
            Input.GetKey(KeyCode.UpArrow))
        {
            cameraPitch += rotateSpeed;
            cameraChanged = true;
        }

        // Look downward
        if (Input.GetKey(KeyCode.S) ||
            Input.GetKey(KeyCode.DownArrow))
        {
            cameraPitch -= rotateSpeed;
            cameraChanged = true;
        }

        cameraPitch = Mathf.Clamp(
            cameraPitch,
            10f,
            80f
        );

        // Zoom in
        if (Input.GetKey(KeyCode.Q) ||
            Input.GetKey(KeyCode.PageUp))
        {
            cameraDistance -= zoomSpeed;
            cameraChanged = true;
        }

        // Zoom out
        if (Input.GetKey(KeyCode.E) ||
            Input.GetKey(KeyCode.PageDown))
        {
            cameraDistance += zoomSpeed;
            cameraChanged = true;
        }

        cameraDistance = Mathf.Clamp(
            cameraDistance,
            7f,
            25f
        );

        // Reset camera
        if (Input.GetKeyDown(KeyCode.R))
        {
            cameraYaw = -36f;
            cameraPitch = 25f;
            cameraDistance = 15f;

            cameraChanged = true;
        }

        if (cameraChanged)
            UpdateCameraOrbit();
    }

    // ==========================================
    // LIGHTING
    // ==========================================

    private void SetupLighting()
    {
        Light directional = null;

        foreach (Light light in FindObjectsByType<Light>(
            FindObjectsSortMode.None))
        {
            if (light.type == LightType.Directional)
            {
                directional = light;
                break;
            }
        }

        if (directional == null)
        {
            GameObject lightObject =
                new GameObject("Directional Light");

            directional =
                lightObject.AddComponent<Light>();

            directional.type = LightType.Directional;
        }

        directional.transform.rotation =
            Quaternion.Euler(50f, -30f, 0f);

        directional.intensity = 1.5f;
        directional.color = Color.white;
        directional.shadows = LightShadows.Soft;

        // Neon Rose accent light
        CreatePointLight(
            new Vector3(-3f, 3f, -2f),
            new Color(1f, 0.08f, 0.45f)
        );

        // Cerulean Blue accent light
        CreatePointLight(
            new Vector3(3f, 3f, 2f),
            new Color(0f, 0.48f, 0.9f)
        );
    }

    private void CreatePointLight(
        Vector3 position,
        Color color)
    {
        GameObject lightObject =
            new GameObject("Accent Light");

        lightObject.transform.position = position;

        Light pointLight =
            lightObject.AddComponent<Light>();

        pointLight.type = LightType.Point;
        pointLight.color = color;
        pointLight.intensity = 3f;
        pointLight.range = 6f;
    }

    // ==========================================
    // CUBE CREATION
    // ==========================================

    private GameObject CreateCube(
        string objectName,
        Vector3 position,
        Vector3 scale,
        Material material)
    {
        GameObject obj = GameObject.CreatePrimitive(
            PrimitiveType.Cube
        );

        obj.name = objectName;
        obj.transform.position = position;
        obj.transform.localScale = scale;

        if (material != null)
        {
            obj.GetComponent<Renderer>().sharedMaterial =
                material;
        }

        return obj;
    }

    // ==========================================
    // ENVIRONMENT CREATION
    // ==========================================

    private void CreateEnvironment()
    {
        // Ground plane
        GameObject ground = GameObject.CreatePrimitive(
            PrimitiveType.Plane
        );

        ground.name = "Ground";

        ground.transform.position =
            new Vector3(0f, -0.25f, 0f);

        ground.transform.localScale =
            new Vector3(2f, 1f, 2f);

        ground.GetComponent<Renderer>().sharedMaterial =
            blackMaterial;

        // Main platform
        CreateCube(
            "Main Platform",
            new Vector3(0f, -0.05f, 0f),
            new Vector3(8f, 0.3f, 6f),
            blackMaterial
        );

        // Cerulean Blue platform trim
        CreateCube(
            "Cerulean Platform Trim",
            new Vector3(0f, 0.115f, -2.95f),
            new Vector3(7.8f, 0.04f, 0.08f),
            blueMaterial
        );

        // Neon Rose platform trim
        CreateCube(
            "Neon Rose Platform Trim",
            new Vector3(0f, 0.115f, 2.95f),
            new Vector3(7.8f, 0.04f, 0.08f),
            roseMaterial
        );
    }

    // ==========================================
    // 3D OBJECT CREATION
    // ==========================================

    private void Create3DObjects()
    {
        // 1. CERULEAN BLUE CUBE
        GameObject cube = CreateCube(
            "Cerulean Blue Cube",
            new Vector3(-2.2f, 1.15f, 0f),
            new Vector3(1.5f, 1.5f, 1.5f),
            blueMaterial
        );

        // 2. JET BLACK CAPSULE
        GameObject capsule = GameObject.CreatePrimitive(
            PrimitiveType.Capsule
        );

        capsule.name = "Jet Black Capsule";

        capsule.transform.position =
            new Vector3(0f, 1.15f, 0f);

        capsule.transform.localScale =
            new Vector3(1.2f, 0.75f, 1.2f);

        capsule.GetComponent<Renderer>().sharedMaterial =
            blackMaterial;

        // 3. NEON ROSE PYRAMID
        GameObject pyramid = CreatePyramid(
            "Neon Rose Pyramid",
            new Vector3(2.2f, 0.4f, 0f),
            1.5f,
            1.7f,
            roseMaterial
        );

        // Cube pedestal
        CreateCube(
            "Cube Pedestal",
            new Vector3(-2.2f, 0.25f, 0f),
            new Vector3(1.8f, 0.3f, 1.8f),
            blackMaterial
        );

        // Capsule pedestal
        CreateCube(
            "Capsule Pedestal",
            new Vector3(0f, 0.25f, 0f),
            new Vector3(1.8f, 0.3f, 1.8f),
            blackMaterial
        );

        // Pyramid pedestal
        CreateCube(
            "Pyramid Pedestal",
            new Vector3(2.2f, 0.25f, 0f),
            new Vector3(1.8f, 0.3f, 1.8f),
            blackMaterial
        );

        // Store interactive objects
        objects.Clear();

        objects.Add(cube);
        objects.Add(capsule);
        objects.Add(pyramid);
    }

    // ==========================================
    // CUSTOM PYRAMID MESH
    // ==========================================

    private GameObject CreatePyramid(
        string objectName,
        Vector3 position,
        float baseSize,
        float height,
        Material material)
    {
        GameObject pyramid =
            new GameObject(objectName);

        pyramid.transform.position = position;

        MeshFilter meshFilter =
            pyramid.AddComponent<MeshFilter>();

        MeshRenderer meshRenderer =
            pyramid.AddComponent<MeshRenderer>();

        Mesh mesh = new Mesh();

        mesh.name = objectName + "_Mesh";

        float half = baseSize / 2f;

        mesh.vertices = new Vector3[]
        {
            new Vector3(-half, 0f, -half),
            new Vector3(half, 0f, -half),
            new Vector3(half, 0f, half),
            new Vector3(-half, 0f, half),
            new Vector3(0f, height, 0f)
        };

        mesh.triangles = new int[]
        {
            // Bottom face
            0, 1, 2,
            0, 2, 3,

            // Four triangular faces
            0, 4, 1,
            1, 4, 2,
            2, 4, 3,
            3, 4, 0
        };

        mesh.RecalculateNormals();
        mesh.RecalculateBounds();

        meshFilter.mesh = mesh;
        meshRenderer.sharedMaterial = material;

        generatedMeshes.Add(mesh);

        return pyramid;
    }

    // ==========================================
    // SAVE ORIGINAL TRANSFORMS
    // ==========================================

    private void SaveInitialTransforms()
    {
        initialPositions.Clear();
        initialScales.Clear();
        initialRotations.Clear();

        foreach (GameObject obj in objects)
        {
            initialPositions.Add(
                obj.transform.position
            );

            initialScales.Add(
                obj.transform.localScale
            );

            initialRotations.Add(
                obj.transform.rotation
            );
        }
    }

    // ==========================================
    // SELECTED OBJECT
    // ==========================================

    private GameObject SelectedObject
    {
        get
        {
            if (objects.Count == 0)
                return null;

            return objects[selectedIndex];
        }
    }

    private void SelectNextObject()
    {
        if (objects.Count == 0)
            return;

        selectedIndex =
            (selectedIndex + 1) % objects.Count;
    }

    // ==========================================
    // OBJECT MOVEMENT
    // ==========================================

    private void MoveObject(Vector3 direction)
    {
        if (SelectedObject == null)
            return;

        SelectedObject.transform.position +=
            direction * 0.4f;
    }

    // ==========================================
    // OBJECT ROTATION
    // ==========================================

    private void RotateObject(float angle)
    {
        if (SelectedObject == null)
            return;

        SelectedObject.transform.Rotate(
            Vector3.up,
            angle,
            Space.World
        );
    }

    // ==========================================
    // OBJECT SCALING
    // ==========================================

    private void ScaleObject(float factor)
    {
        if (SelectedObject == null)
            return;

        Vector3 currentScale =
            SelectedObject.transform.localScale;

        Vector3 originalScale =
            initialScales[selectedIndex];

        Vector3 newScale = currentScale * factor;

        // Limit minimum and maximum size
        newScale.x = Mathf.Clamp(
            newScale.x,
            originalScale.x * 0.25f,
            originalScale.x * 3f
        );

        newScale.y = Mathf.Clamp(
            newScale.y,
            originalScale.y * 0.25f,
            originalScale.y * 3f
        );

        newScale.z = Mathf.Clamp(
            newScale.z,
            originalScale.z * 0.25f,
            originalScale.z * 3f
        );

        SelectedObject.transform.localScale = newScale;
    }

    // Scale up by 15%
    private void ScaleUp()
    {
        ScaleObject(1.15f);
    }

    // Scale down by 15%
    private void ScaleDown()
    {
        ScaleObject(0.85f);
    }

    // ==========================================
    // RESET OBJECT SIZE
    // ==========================================

    private void ResetObjectSize()
    {
        if (SelectedObject == null)
            return;

        SelectedObject.transform.localScale =
            initialScales[selectedIndex];
    }

    // ==========================================
    // RESET SELECTED OBJECT
    // ==========================================

    private void ResetObject()
    {
        if (SelectedObject == null)
            return;

        SelectedObject.transform.position =
            initialPositions[selectedIndex];

        SelectedObject.transform.localScale =
            initialScales[selectedIndex];

        SelectedObject.transform.rotation =
            initialRotations[selectedIndex];
    }

    // ==========================================
    // UPDATE
    // ==========================================

    private void Update()
    {
        HandleCameraControls();
    }

    // ==========================================
    // INTERACTIVE MENU
    // ==========================================

    private void OnGUI()
    {
        float panelWidth = 280f;

        float panelHeight =
            Mathf.Max(200f, Screen.height - 30f);

        GUILayout.BeginArea(
            new Rect(
                15f,
                15f,
                panelWidth,
                panelHeight
            ),
            "EXPERIMENT 9 - 3D SCENE",
            GUI.skin.window
        );

        menuScrollPosition = GUILayout.BeginScrollView(
            menuScrollPosition,
            false,
            true,
            GUILayout.Width(panelWidth - 15f),
            GUILayout.Height(panelHeight - 35f)
        );

        GUILayout.Label(
            "Interactive 3D Environment"
        );

        GUILayout.Space(8);

        if (SelectedObject != null)
        {
            GUILayout.Label(
                "Selected: " + SelectedObject.name
            );
        }

        if (GUILayout.Button("Select Next Object"))
            SelectNextObject();

        // ======================================
        // OBJECT SCALING
        // ======================================

        GUILayout.Space(8);

        GUILayout.Label("OBJECT SCALING");

        if (GUILayout.Button("Scale Up"))
            ScaleUp();

        if (GUILayout.Button("Scale Down"))
            ScaleDown();

        if (GUILayout.Button("Reset Object Size"))
            ResetObjectSize();

        // ======================================
        // OBJECT MOVEMENT
        // ======================================

        GUILayout.Space(8);

        GUILayout.Label("OBJECT MOVEMENT");

        if (GUILayout.Button("Move Left"))
            MoveObject(Vector3.left);

        if (GUILayout.Button("Move Right"))
            MoveObject(Vector3.right);

        if (GUILayout.Button("Move Forward"))
            MoveObject(Vector3.forward);

        if (GUILayout.Button("Move Backward"))
            MoveObject(Vector3.back);

        // ======================================
        // OBJECT ROTATION
        // ======================================

        GUILayout.Space(8);

        GUILayout.Label("OBJECT ROTATION");

        if (GUILayout.Button("Rotate Left"))
            RotateObject(-20f);

        if (GUILayout.Button("Rotate Right"))
            RotateObject(20f);

        // Reset immediately follows rotation
        GUILayout.Space(3);

        if (GUILayout.Button("Reset Selected Object"))
            ResetObject();

        GUILayout.EndScrollView();

        GUILayout.EndArea();
    }

    // ==========================================
    // CLEANUP
    // ==========================================

    private void OnDestroy()
    {
        if (blackMaterial != null)
            Destroy(blackMaterial);

        if (blueMaterial != null)
            Destroy(blueMaterial);

        if (roseMaterial != null)
            Destroy(roseMaterial);

        foreach (Mesh mesh in generatedMeshes)
        {
            if (mesh != null)
                Destroy(mesh);
        }

        generatedMeshes.Clear();
    }
}
