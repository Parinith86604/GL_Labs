
using System;
using UnityEngine;

#if ENABLE_INPUT_SYSTEM
using UnityEngine.InputSystem;
#endif

public class Experiment10Controller : MonoBehaviour
{
    // Colour palette
    private static readonly Color JetBlack =
        new Color32(13, 13, 18, 255);

    private static readonly Color CeruleanBlue =
        new Color32(0, 123, 167, 255);

    private static readonly Color NeonRose =
        new Color32(255, 46, 147, 255);

    private const float PivotX = 0.5f;
    private const float PivotY = 0.5f;

    // Polygon
    private GameObject polygonObject;
    private Mesh polygonMesh;
    private LineRenderer polygonOutline;

    private Vector3[] originalVertices;
    private Vector3[] currentVertices;

    private Material polygonMaterial;
    private Material outlineMaterial;
    private Texture2D blendedTexture;

    // Camera
    private Camera sceneCamera;

    private float cameraYaw;
    private float cameraPitch;
    private float cameraDistance = 10f;

    private bool insetViewport;
    private bool continuousRotation;

    private const float MinCameraDistance = 6f;
    private const float MaxCameraDistance = 16f;

    // Interface
    private Vector2 menuScrollPosition;

    // ============================================
    // START
    // ============================================

    void Start()
    {
        SetupCamera();
        CreatePolygon();
        UpdateCameraTransform();
    }

    void Update()
    {
        HandleKeyboardInput();

        if (continuousRotation && polygonMesh != null)
        {
            ApplyMatrix(
                RotationMatrix(45f * Time.deltaTime)
            );
        }
    }

    void LateUpdate()
    {
        UpdateCameraTransform();
    }

    // ============================================
    // KEYBOARD INPUT SUPPORT
    // ============================================

#if ENABLE_INPUT_SYSTEM
    Key ConvertKey(KeyCode code)
    {
        switch (code)
        {
            case KeyCode.A: return Key.A;
            case KeyCode.B: return Key.B;
            case KeyCode.C: return Key.C;
            case KeyCode.D: return Key.D;
            case KeyCode.E: return Key.E;
            case KeyCode.I: return Key.I;
            case KeyCode.J: return Key.J;
            case KeyCode.K: return Key.K;
            case KeyCode.L: return Key.L;
            case KeyCode.M: return Key.M;
            case KeyCode.N: return Key.N;
            case KeyCode.P: return Key.P;
            case KeyCode.Q: return Key.Q;
            case KeyCode.R: return Key.R;
            case KeyCode.S: return Key.S;
            case KeyCode.V: return Key.V;
            case KeyCode.W: return Key.W;
            case KeyCode.X: return Key.X;
            case KeyCode.Z: return Key.Z;

            case KeyCode.Alpha0: return Key.Digit0;
            case KeyCode.Alpha1: return Key.Digit1;
            case KeyCode.Alpha2: return Key.Digit2;
            case KeyCode.Alpha3: return Key.Digit3;
            case KeyCode.Alpha4: return Key.Digit4;
            case KeyCode.Alpha5: return Key.Digit5;
            case KeyCode.Alpha6: return Key.Digit6;
            case KeyCode.Alpha7: return Key.Digit7;
            case KeyCode.Alpha8: return Key.Digit8;
            case KeyCode.Alpha9: return Key.Digit9;

            case KeyCode.LeftArrow: return Key.LeftArrow;
            case KeyCode.RightArrow: return Key.RightArrow;
            case KeyCode.UpArrow: return Key.UpArrow;
            case KeyCode.DownArrow: return Key.DownArrow;
            case KeyCode.Backspace: return Key.Backspace;
        }

        return Key.None;
    }
#endif

    bool KeyHeld(KeyCode code)
    {
#if ENABLE_INPUT_SYSTEM
        if (Keyboard.current != null)
        {
            Key key = ConvertKey(code);

            if (key != Key.None &&
                Keyboard.current[key].isPressed)
                return true;
        }
#endif

#if ENABLE_LEGACY_INPUT_MANAGER
        return Input.GetKey(code);
#else
        return false;
#endif
    }

    bool KeyDown(KeyCode code)
    {
#if ENABLE_INPUT_SYSTEM
        if (Keyboard.current != null)
        {
            Key key = ConvertKey(code);

            if (key != Key.None &&
                Keyboard.current[key].wasPressedThisFrame)
                return true;
        }
#endif

#if ENABLE_LEGACY_INPUT_MANAGER
        return Input.GetKeyDown(code);
#else
        return false;
#endif
    }

    // ============================================
    // CAMERA SETUP
    // ============================================

    void SetupCamera()
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

        sceneCamera.clearFlags =
            CameraClearFlags.SolidColor;

        sceneCamera.backgroundColor =
            new Color(0.12f, 0.12f, 0.13f, 1f);

        sceneCamera.orthographic = true;
        sceneCamera.orthographicSize = 3.7f;
        sceneCamera.fieldOfView = 42f;

        sceneCamera.nearClipPlane = 0.1f;
        sceneCamera.farClipPlane = 100f;
        sceneCamera.allowMSAA = true;

        QualitySettings.antiAliasing = 8;
        Application.targetFrameRate = 60;
    }

    void PositionPolygonBesideMenu()
    {
        if (polygonObject == null ||
            sceneCamera == null)
            return;

        float screenWidth = Mathf.Max(Screen.width, 1);
        float screenHeight = Mathf.Max(Screen.height, 1);

        float panelWidth =
            Mathf.Min(310f, screenWidth * 0.34f);

        float halfWidth =
            sceneCamera.orthographicSize *
            screenWidth / screenHeight;

        float panelWorldWidth =
            panelWidth / screenWidth * halfWidth * 2f;

        float centerX = panelWorldWidth * 0.5f;

        polygonObject.transform.position =
            new Vector3(centerX, 0f, 0f);
    }

    void UpdateCameraTransform()
    {
        if (sceneCamera == null)
            return;

        Vector3 target =
            polygonObject != null
                ? polygonObject.transform.position
                : Vector3.zero;

        Quaternion orbit =
            Quaternion.Euler(cameraPitch, cameraYaw, 0f);

        Vector3 offset =
            orbit * new Vector3(0f, 0f, -cameraDistance);

        sceneCamera.transform.position = target + offset;

        sceneCamera.transform.rotation =
            Quaternion.LookRotation(
                target - sceneCamera.transform.position,
                Vector3.up
            );
    }

    void ResetCamera()
    {
        cameraYaw = 0f;
        cameraPitch = 0f;
        cameraDistance = 10f;

        sceneCamera.orthographic = true;
        sceneCamera.orthographicSize = 3.7f;

        sceneCamera.rect = new Rect(0f, 0f, 1f, 1f);
        insetViewport = false;
    }

    void ZoomIn()
    {
        if (sceneCamera.orthographic)
        {
            sceneCamera.orthographicSize =
                Mathf.Clamp(
                    sceneCamera.orthographicSize - 0.3f,
                    2.3f,
                    6f
                );
        }
        else
        {
            cameraDistance =
                Mathf.Clamp(
                    cameraDistance - 0.5f,
                    MinCameraDistance,
                    MaxCameraDistance
                );
        }
    }

    void ZoomOut()
    {
        if (sceneCamera.orthographic)
        {
            sceneCamera.orthographicSize =
                Mathf.Clamp(
                    sceneCamera.orthographicSize + 0.3f,
                    2.3f,
                    6f
                );
        }
        else
        {
            cameraDistance =
                Mathf.Clamp(
                    cameraDistance + 0.5f,
                    MinCameraDistance,
                    MaxCameraDistance
                );
        }
    }

    void ToggleProjection()
    {
        sceneCamera.orthographic =
            !sceneCamera.orthographic;
    }

    void ToggleViewport()
    {
        insetViewport = !insetViewport;

        sceneCamera.rect = insetViewport
            ? new Rect(0.1f, 0.1f, 0.8f, 0.8f)
            : new Rect(0f, 0f, 1f, 1f);
    }

    // ============================================
    // CREATE POLYGON
    // ============================================

    void CreatePolygon()
    {
        polygonObject =
            new GameObject("Transformation Polygon");

        MeshFilter meshFilter =
            polygonObject.AddComponent<MeshFilter>();

        MeshRenderer meshRenderer =
            polygonObject.AddComponent<MeshRenderer>();

        // Symmetrical octagon
        Vector3[] boundary =
        {
            new Vector3(-0.65f, -1.50f, 0f),
            new Vector3( 0.65f, -1.50f, 0f),
            new Vector3( 1.50f, -0.65f, 0f),
            new Vector3( 1.50f,  0.65f, 0f),
            new Vector3( 0.65f,  1.50f, 0f),
            new Vector3(-0.65f,  1.50f, 0f),
            new Vector3(-1.50f,  0.65f, 0f),
            new Vector3(-1.50f, -0.65f, 0f)
        };

        originalVertices =
            new Vector3[boundary.Length + 1];

        originalVertices[0] = Vector3.zero;

        for (int i = 0; i < boundary.Length; i++)
            originalVertices[i + 1] = boundary[i];

        currentVertices =
            (Vector3[])originalVertices.Clone();

        int[] triangles =
            new int[boundary.Length * 3];

        for (int i = 0; i < boundary.Length; i++)
        {
            int next = (i + 1) % boundary.Length;

            triangles[i * 3] = 0;
            triangles[i * 3 + 1] = next + 1;
            triangles[i * 3 + 2] = i + 1;
        }

        Vector2[] uv =
            new Vector2[originalVertices.Length];

        uv[0] = new Vector2(0.5f, 0.5f);

        for (int i = 0; i < boundary.Length; i++)
        {
            uv[i + 1] = new Vector2(
                Mathf.InverseLerp(-1.5f, 1.5f, boundary[i].x),
                Mathf.InverseLerp(-1.5f, 1.5f, boundary[i].y)
            );
        }

        polygonMesh = new Mesh();
        polygonMesh.name =
            "Experiment 10 Transformation Polygon";

        polygonMesh.vertices = currentVertices;
        polygonMesh.triangles = triangles;
        polygonMesh.uv = uv;

        polygonMesh.RecalculateNormals();
        polygonMesh.RecalculateBounds();

        meshFilter.sharedMesh = polygonMesh;

        polygonMaterial = CreateBlendedMaterial();
        meshRenderer.sharedMaterial = polygonMaterial;

        CreatePolygonOutline(boundary);

        PositionPolygonBesideMenu();
    }

    // ============================================
    // BLENDED COLOUR MATERIAL
    // ============================================

    Material CreateBlendedMaterial()
    {
        Shader shader =
            Shader.Find("Universal Render Pipeline/Unlit");

        if (shader == null)
            shader = Shader.Find("Unlit/Texture");

        if (shader == null)
            shader = Shader.Find("Sprites/Default");

        if (shader == null)
            shader = Shader.Find("Standard");

        if (shader == null)
            throw new Exception("Suitable shader not found.");

        Material material = new Material(shader);

        blendedTexture = CreateBlendedTexture();

        if (material.HasProperty("_BaseMap"))
            material.SetTexture("_BaseMap", blendedTexture);

        if (material.HasProperty("_MainTex"))
            material.SetTexture("_MainTex", blendedTexture);

        if (material.HasProperty("_Cull"))
            material.SetFloat("_Cull", 0f);

        material.color = Color.white;

        return material;
    }

    Texture2D CreateBlendedTexture()
    {
        const int size = 1024;

        Texture2D texture = new Texture2D(
            size,
            size,
            TextureFormat.RGBA32,
            true
        );

        texture.name = "Blended Three Colour Texture";
        texture.filterMode = FilterMode.Trilinear;
        texture.wrapMode = TextureWrapMode.Clamp;
        texture.anisoLevel = 8;

        Color[] pixels = new Color[size * size];

        for (int y = 0; y < size; y++)
        {
            for (int x = 0; x < size; x++)
            {
                float u = (float)x / (size - 1);
                float v = (float)y / (size - 1);

                float blackWeight = (1f - u) * (1f - v);

                float blueWeight =
                    u * (1f - v) +
                    (1f - u) * v;

                float roseWeight = u * v;

                Color finalColor =
                    JetBlack * blackWeight +
                    CeruleanBlue * blueWeight +
                    NeonRose * roseWeight;

                pixels[y * size + x] = finalColor;
            }
        }

        texture.SetPixels(pixels);
        texture.Apply(true, false);

        return texture;
    }

    // ============================================
    // POLYGON OUTLINE
    // ============================================

    void CreatePolygonOutline(Vector3[] boundary)
    {
        GameObject outlineObject =
            new GameObject("Polygon Outline");

        outlineObject.transform.SetParent(
            polygonObject.transform,
            false
        );

        polygonOutline =
            outlineObject.AddComponent<LineRenderer>();

        Shader shader =
            Shader.Find("Universal Render Pipeline/Unlit");

        if (shader == null)
            shader = Shader.Find("Sprites/Default");

        outlineMaterial = new Material(shader);

        polygonOutline.material = outlineMaterial;
        polygonOutline.useWorldSpace = false;
        polygonOutline.loop = true;

        polygonOutline.positionCount = boundary.Length;

        polygonOutline.startWidth = 0.035f;
        polygonOutline.endWidth = 0.035f;

        polygonOutline.numCornerVertices = 4;
        polygonOutline.numCapVertices = 4;

        Gradient gradient = new Gradient();

        gradient.SetKeys(
            new GradientColorKey[]
            {
                new GradientColorKey(CeruleanBlue, 0f),
                new GradientColorKey(NeonRose, 0.5f),
                new GradientColorKey(CeruleanBlue, 1f)
            },
            new GradientAlphaKey[]
            {
                new GradientAlphaKey(1f, 0f),
                new GradientAlphaKey(1f, 1f)
            }
        );

        polygonOutline.colorGradient = gradient;

        polygonOutline.shadowCastingMode =
            UnityEngine.Rendering.ShadowCastingMode.Off;

        polygonOutline.receiveShadows = false;

        for (int i = 0; i < boundary.Length; i++)
        {
            polygonOutline.SetPosition(
                i,
                boundary[i] + new Vector3(0f, 0f, -0.035f)
            );
        }
    }

    // ============================================
    // MATRIX MULTIPLICATION
    // ============================================

    float[,] MultiplyMatrices(float[,] a, float[,] b)
    {
        int rows = a.GetLength(0);
        int common = a.GetLength(1);
        int columns = b.GetLength(1);

        if (common != b.GetLength(0))
            throw new ArgumentException(
                "Invalid matrix dimensions."
            );

        float[,] result = new float[rows, columns];

        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < columns; j++)
            {
                for (int k = 0; k < common; k++)
                    result[i, j] += a[i, k] * b[k, j];
            }
        }

        return result;
    }

    // ============================================
    // APPLY MATRIX
    // ============================================

    void ApplyMatrix(float[,] matrix)
    {
        if (polygonMesh == null)
            return;

        Vector3[] transformed =
            new Vector3[currentVertices.Length];

        for (int i = 0; i < currentVertices.Length; i++)
        {
            float[,] point =
            {
                { currentVertices[i].x },
                { currentVertices[i].y },
                { 1f }
            };

            float[,] result =
                MultiplyMatrices(matrix, point);

            transformed[i] = new Vector3(
                result[0, 0],
                result[1, 0],
                currentVertices[i].z
            );
        }

        currentVertices = transformed;

        polygonMesh.vertices = currentVertices;
        polygonMesh.RecalculateNormals();
        polygonMesh.RecalculateBounds();

        UpdatePolygonOutline();
    }

    void UpdatePolygonOutline()
    {
        if (polygonOutline == null)
            return;

        for (int i = 0; i < currentVertices.Length - 1; i++)
        {
            polygonOutline.SetPosition(
                i,
                currentVertices[i + 1] +
                new Vector3(0f, 0f, -0.035f)
            );
        }
    }

    // ============================================
    // TRANSLATION
    // ============================================

    float[,] TranslationMatrix(float tx, float ty)
    {
        return new float[,]
        {
            { 1f, 0f, tx },
            { 0f, 1f, ty },
            { 0f, 0f, 1f }
        };
    }

    // ============================================
    // ROTATION
    // ============================================

    float[,] RotationMatrix(float angle)
    {
        float radians = angle * Mathf.Deg2Rad;

        float c = Mathf.Cos(radians);
        float s = Mathf.Sin(radians);

        return new float[,]
        {
            { c, -s, 0f },
            { s,  c, 0f },
            { 0f, 0f, 1f }
        };
    }

    // ============================================
    // SCALING
    // ============================================

    float[,] ScalingMatrix(float sx, float sy)
    {
        return new float[,]
        {
            { sx, 0f, 0f },
            { 0f, sy, 0f },
            { 0f, 0f, 1f }
        };
    }

    // ============================================
    // REFLECTION
    // ============================================

    float[,] ReflectionX()
    {
        return ScalingMatrix(1f, -1f);
    }

    float[,] ReflectionY()
    {
        return ScalingMatrix(-1f, 1f);
    }

    float[,] ReflectionOrigin()
    {
        return ScalingMatrix(-1f, -1f);
    }

    float[,] ReflectionYX()
    {
        return new float[,]
        {
            { 0f, 1f, 0f },
            { 1f, 0f, 0f },
            { 0f, 0f, 1f }
        };
    }

    // ============================================
    // SHEARING
    // ============================================

    float[,] ShearX(float amount)
    {
        return new float[,]
        {
            { 1f, amount, 0f },
            { 0f, 1f, 0f },
            { 0f, 0f, 1f }
        };
    }

    float[,] ShearY(float amount)
    {
        return new float[,]
        {
            { 1f, 0f, 0f },
            { amount, 1f, 0f },
            { 0f, 0f, 1f }
        };
    }

    // ============================================
    // ARBITRARY PIVOT ROTATION
    // ============================================

    float[,] RotationAboutPivot(
        float angle, float px, float py)
    {
        float[,] moveToOrigin =
            TranslationMatrix(-px, -py);

        float[,] rotation =
            RotationMatrix(angle);

        float[,] moveBack =
            TranslationMatrix(px, py);

        return MultiplyMatrices(
            moveBack,
            MultiplyMatrices(rotation, moveToOrigin)
        );
    }

    // ============================================
    // COMPOSITE TRANSFORMATION
    // ============================================

    void ApplyCompositeTransformation()
    {
        float[,] scale = ScalingMatrix(1.15f, 0.85f);
        float[,] rotate = RotationMatrix(25f);
        float[,] translate = TranslationMatrix(0.35f, 0.2f);

        float[,] composite = MultiplyMatrices(
            translate,
            MultiplyMatrices(rotate, scale)
        );

        ApplyMatrix(composite);
    }

    // ============================================
    // RESET POLYGON
    // ============================================

    void ResetPolygon()
    {
        continuousRotation = false;

        if (polygonMesh == null)
            return;

        currentVertices =
            (Vector3[])originalVertices.Clone();

        polygonMesh.vertices = currentVertices;

        polygonMesh.RecalculateNormals();
        polygonMesh.RecalculateBounds();

        polygonObject.transform.rotation =
            Quaternion.identity;

        UpdatePolygonOutline();
    }

    // ============================================
    // OBJECT ROTATION
    // ============================================

    void TiltObjectUp()
    {
        polygonObject.transform.Rotate(
            Vector3.right, -10f, Space.World
        );
    }

    void TiltObjectDown()
    {
        polygonObject.transform.Rotate(
            Vector3.right, 10f, Space.World
        );
    }

    void TiltObjectLeft()
    {
        polygonObject.transform.Rotate(
            Vector3.up, -10f, Space.World
        );
    }

    void TiltObjectRight()
    {
        polygonObject.transform.Rotate(
            Vector3.up, 10f, Space.World
        );
    }

    void ResetObjectTilt()
    {
        polygonObject.transform.rotation =
            Quaternion.identity;
    }

    // ============================================
    // KEYBOARD CONTROLS
    // ============================================

    void HandleKeyboardInput()
    {
        float cameraSpeed = 65f * Time.deltaTime;
        float objectSpeed = 60f * Time.deltaTime;

        // Camera movement
        if (KeyHeld(KeyCode.A))
            cameraYaw -= cameraSpeed;

        if (KeyHeld(KeyCode.D))
            cameraYaw += cameraSpeed;

        if (KeyHeld(KeyCode.W))
            cameraPitch = Mathf.Clamp(
                cameraPitch - cameraSpeed, -55f, 55f
            );

        if (KeyHeld(KeyCode.S))
            cameraPitch = Mathf.Clamp(
                cameraPitch + cameraSpeed, -55f, 55f
            );

        if (KeyHeld(KeyCode.Q))
            ZoomIn();

        if (KeyHeld(KeyCode.E))
            ZoomOut();

        if (KeyDown(KeyCode.R))
            ResetCamera();

        // Object tilt
        if (KeyHeld(KeyCode.I))
        {
            polygonObject.transform.Rotate(
                Vector3.right, -objectSpeed, Space.World
            );
        }

        if (KeyHeld(KeyCode.K))
        {
            polygonObject.transform.Rotate(
                Vector3.right, objectSpeed, Space.World
            );
        }

        if (KeyHeld(KeyCode.J))
        {
            polygonObject.transform.Rotate(
                Vector3.up, -objectSpeed, Space.World
            );
        }

        if (KeyHeld(KeyCode.L))
        {
            polygonObject.transform.Rotate(
                Vector3.up, objectSpeed, Space.World
            );
        }

        // Translation with arrow keys
        if (KeyDown(KeyCode.LeftArrow))
            ApplyMatrix(TranslationMatrix(-0.4f, 0f));

        if (KeyDown(KeyCode.RightArrow))
            ApplyMatrix(TranslationMatrix(0.4f, 0f));

        if (KeyDown(KeyCode.UpArrow))
            ApplyMatrix(TranslationMatrix(0f, 0.4f));

        if (KeyDown(KeyCode.DownArrow))
            ApplyMatrix(TranslationMatrix(0f, -0.4f));

        // Rotation
        if (KeyDown(KeyCode.Z))
            ApplyMatrix(RotationMatrix(15f));

        if (KeyDown(KeyCode.X))
            ApplyMatrix(RotationMatrix(-15f));

        // Arbitrary pivot
        if (KeyDown(KeyCode.C))
            ApplyMatrix(
                RotationAboutPivot(15f, PivotX, PivotY)
            );

        if (KeyDown(KeyCode.V))
            ApplyMatrix(
                RotationAboutPivot(-15f, PivotX, PivotY)
            );

        // Scaling
        if (KeyDown(KeyCode.Alpha1))
            ApplyMatrix(ScalingMatrix(1.2f, 1f));

        if (KeyDown(KeyCode.Alpha2))
            ApplyMatrix(ScalingMatrix(0.8f, 1f));

        if (KeyDown(KeyCode.Alpha3))
            ApplyMatrix(ScalingMatrix(1f, 1.2f));

        if (KeyDown(KeyCode.Alpha4))
            ApplyMatrix(ScalingMatrix(1f, 0.8f));

        // Reflection
        if (KeyDown(KeyCode.Alpha5))
            ApplyMatrix(ReflectionX());

        if (KeyDown(KeyCode.Alpha6))
            ApplyMatrix(ReflectionY());

        if (KeyDown(KeyCode.Alpha7))
            ApplyMatrix(ReflectionOrigin());

        if (KeyDown(KeyCode.Alpha8))
            ApplyMatrix(ReflectionYX());

        // Shearing
        if (KeyDown(KeyCode.Alpha9))
            ApplyMatrix(ShearX(0.3f));

        if (KeyDown(KeyCode.Alpha0))
            ApplyMatrix(ShearY(0.3f));

        // Continuous rotation
        if (KeyDown(KeyCode.B))
            continuousRotation = !continuousRotation;

        // Composite transformation
        if (KeyDown(KeyCode.N))
            ApplyCompositeTransformation();

        // Reset
        if (KeyDown(KeyCode.Backspace))
            ResetPolygon();

        // Projection and viewport mapping
        if (KeyDown(KeyCode.P))
            ToggleProjection();

        if (KeyDown(KeyCode.M))
            ToggleViewport();
    }

    // ============================================
    // REMAINING PANELS
    // 3D VIEWING CONTROLS PANEL REMOVED
    // ============================================

    void OnGUI()
    {
        GUILayout.BeginArea(
            new Rect(10, 10, 310, Screen.height - 20),
            GUI.skin.box
        );

        GUILayout.Label("EXPERIMENT 10");
        GUILayout.Label("GEOMETRIC TRANSFORMATIONS");

        menuScrollPosition = GUILayout.BeginScrollView(
            menuScrollPosition
        );

        // OBJECT ROTATION
        GUILayout.Space(8);
        GUILayout.Label("OBJECT ROTATION");

        if (GUILayout.Button("Rotate Object Up"))
            TiltObjectUp();

        if (GUILayout.Button("Rotate Object Down"))
            TiltObjectDown();

        if (GUILayout.Button("Rotate Object Left"))
            TiltObjectLeft();

        if (GUILayout.Button("Rotate Object Right"))
            TiltObjectRight();

        if (GUILayout.Button("Reset Object Tilt"))
            ResetObjectTilt();

        // TRANSLATION
        GUILayout.Space(8);
        GUILayout.Label("TRANSLATION");

        if (GUILayout.Button("Translate Left"))
            ApplyMatrix(TranslationMatrix(-0.5f, 0f));

        if (GUILayout.Button("Translate Right"))
            ApplyMatrix(TranslationMatrix(0.5f, 0f));

        if (GUILayout.Button("Translate Up"))
            ApplyMatrix(TranslationMatrix(0f, 0.5f));

        if (GUILayout.Button("Translate Down"))
            ApplyMatrix(TranslationMatrix(0f, -0.5f));

        // ROTATION
        GUILayout.Space(8);
        GUILayout.Label("ROTATION");

        if (GUILayout.Button("Rotate +15 Degrees"))
            ApplyMatrix(RotationMatrix(15f));

        if (GUILayout.Button("Rotate -15 Degrees"))
            ApplyMatrix(RotationMatrix(-15f));

        // ARBITRARY PIVOT ROTATION
        GUILayout.Space(8);
        GUILayout.Label("ARBITRARY PIVOT ROTATION");

        if (GUILayout.Button("Rotate About Pivot +15"))
        {
            ApplyMatrix(
                RotationAboutPivot(15f, PivotX, PivotY)
            );
        }

        if (GUILayout.Button("Rotate About Pivot -15"))
        {
            ApplyMatrix(
                RotationAboutPivot(-15f, PivotX, PivotY)
            );
        }

        // NON-UNIFORM SCALING
        GUILayout.Space(8);
        GUILayout.Label("NON-UNIFORM SCALING");

        if (GUILayout.Button("Scale X Up"))
            ApplyMatrix(ScalingMatrix(1.2f, 1f));

        if (GUILayout.Button("Scale Y Up"))
            ApplyMatrix(ScalingMatrix(1f, 1.2f));

        if (GUILayout.Button("Scale X Down"))
            ApplyMatrix(ScalingMatrix(0.8f, 1f));

        if (GUILayout.Button("Scale Y Down"))
            ApplyMatrix(ScalingMatrix(1f, 0.8f));

        // REFLECTION
        GUILayout.Space(8);
        GUILayout.Label("REFLECTION");

        if (GUILayout.Button("Reflect About X-Axis"))
            ApplyMatrix(ReflectionX());

        if (GUILayout.Button("Reflect About Y-Axis"))
            ApplyMatrix(ReflectionY());

        if (GUILayout.Button("Reflect About Origin"))
            ApplyMatrix(ReflectionOrigin());

        if (GUILayout.Button("Reflect About y = x"))
            ApplyMatrix(ReflectionYX());

        // SHEARING
        GUILayout.Space(8);
        GUILayout.Label("SHEARING");

        if (GUILayout.Button("Shear Along X"))
            ApplyMatrix(ShearX(0.3f));

        if (GUILayout.Button("Shear Along Y"))
            ApplyMatrix(ShearY(0.3f));

        // COMPOSITE TRANSFORMATION
        GUILayout.Space(8);
        GUILayout.Label("COMPOSITE TRANSFORMATION");

        if (GUILayout.Button("Apply Composite Transformation"))
            ApplyCompositeTransformation();

        // CONTINUOUS ROTATION
        GUILayout.Space(8);
        GUILayout.Label("CONTINUOUS ROTATION");

        if (GUILayout.Button(
            continuousRotation
                ? "Stop Rotation"
                : "Start Rotation"))
        {
            continuousRotation = !continuousRotation;
        }

        // RESET
        GUILayout.Space(8);

        if (GUILayout.Button("Reset Polygon"))
            ResetPolygon();

        GUILayout.EndScrollView();
        GUILayout.EndArea();
    }

    // ============================================
    // CLEANUP
    // ============================================

    void OnDestroy()
    {
        if (blendedTexture != null)
            Destroy(blendedTexture);

        if (polygonMaterial != null)
            Destroy(polygonMaterial);

        if (outlineMaterial != null)
            Destroy(outlineMaterial);

        if (polygonMesh != null)
            Destroy(polygonMesh);
    }
}
