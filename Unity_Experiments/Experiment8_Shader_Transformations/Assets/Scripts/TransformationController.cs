
using UnityEngine;

[RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
public class TransformationController : MonoBehaviour
{
    [Header("Shader")]
    [SerializeField] private Shader polygonShader;

    [Header("Polygon Settings")]
    [SerializeField] private int sides = 5;
    [SerializeField] private float radius = 1.4f;
    [SerializeField]
    private Color polygonColor =
        new Color(0.15f, 0.65f, 1f, 1f);

    private Mesh polygonMesh;
    private Material polygonMaterial;
    private MeshFilter meshFilter;
    private MeshRenderer meshRenderer;
    private Vector3[] originalVertices;

    private Matrix3x3 currentMatrix = Matrix3x3.Identity;
    private bool animateRotation;
    private string currentOperation = "Original";

    private struct Matrix3x3
    {
        public float m00, m01, m02;
        public float m10, m11, m12;
        public float m20, m21, m22;

        public static Matrix3x3 Identity
        {
            get
            {
                return new Matrix3x3
                {
                    m00 = 1,
                    m01 = 0,
                    m02 = 0,
                    m10 = 0,
                    m11 = 1,
                    m12 = 0,
                    m20 = 0,
                    m21 = 0,
                    m22 = 1
                };
            }
        }

        public static Matrix3x3 Translation(float tx, float ty)
        {
            Matrix3x3 matrix = Identity;
            matrix.m02 = tx;
            matrix.m12 = ty;
            return matrix;
        }

        public static Matrix3x3 Rotation(float degrees)
        {
            float angle = degrees * Mathf.Deg2Rad;
            float c = Mathf.Cos(angle);
            float s = Mathf.Sin(angle);

            Matrix3x3 matrix = Identity;
            matrix.m00 = c;
            matrix.m01 = -s;
            matrix.m10 = s;
            matrix.m11 = c;

            return matrix;
        }

        // Rotation around an arbitrary pivot point.
        public static Matrix3x3 RotationAboutPoint(
            float degrees, float px, float py)
        {
            return Translation(px, py)
                 * Rotation(degrees)
                 * Translation(-px, -py);
        }

        public static Matrix3x3 Scaling(float sx, float sy)
        {
            Matrix3x3 matrix = Identity;
            matrix.m00 = sx;
            matrix.m11 = sy;
            return matrix;
        }

        public static Matrix3x3 ReflectionX()
        {
            return Scaling(1f, -1f);
        }

        // Reflection about the line y = x.
        public static Matrix3x3 ReflectionYEqualsX()
        {
            Matrix3x3 matrix = Identity;

            matrix.m00 = 0;
            matrix.m01 = 1;
            matrix.m10 = 1;
            matrix.m11 = 0;

            return matrix;
        }

        public static Matrix3x3 Shearing(float factor)
        {
            Matrix3x3 matrix = Identity;
            matrix.m01 = factor;
            return matrix;
        }

        public Vector3 MultiplyPoint(Vector3 point)
        {
            float x = m00 * point.x + m01 * point.y + m02;
            float y = m10 * point.x + m11 * point.y + m12;
            float w = m20 * point.x + m21 * point.y + m22;

            if (Mathf.Abs(w) > Mathf.Epsilon)
            {
                x /= w;
                y /= w;
            }

            return new Vector3(x, y, point.z);
        }

        public static Matrix3x3 operator *(Matrix3x3 a, Matrix3x3 b)
        {
            Matrix3x3 r = new Matrix3x3();

            r.m00 = a.m00 * b.m00 + a.m01 * b.m10 + a.m02 * b.m20;
            r.m01 = a.m00 * b.m01 + a.m01 * b.m11 + a.m02 * b.m21;
            r.m02 = a.m00 * b.m02 + a.m01 * b.m12 + a.m02 * b.m22;

            r.m10 = a.m10 * b.m00 + a.m11 * b.m10 + a.m12 * b.m20;
            r.m11 = a.m10 * b.m01 + a.m11 * b.m11 + a.m12 * b.m21;
            r.m12 = a.m10 * b.m02 + a.m11 * b.m12 + a.m12 * b.m22;

            r.m20 = a.m20 * b.m00 + a.m21 * b.m10 + a.m22 * b.m20;
            r.m21 = a.m20 * b.m01 + a.m21 * b.m11 + a.m22 * b.m21;
            r.m22 = a.m20 * b.m02 + a.m21 * b.m12 + a.m22 * b.m22;

            return r;
        }
    }

    private void Start()
    {
        meshFilter = GetComponent<MeshFilter>();
        meshRenderer = GetComponent<MeshRenderer>();

        transform.localPosition = new Vector3(2f, 0f, 0f);

        CreatePolygon();
        CreatePolygonMaterial();
        ApplyTransformation();
    }

    private void CreatePolygon()
    {
        if (sides < 3)
        {
            Debug.LogError("A polygon must have at least three sides.");
            return;
        }

        originalVertices = new Vector3[sides + 1];
        originalVertices[0] = Vector3.zero;

        for (int i = 0; i < sides; i++)
        {
            float angle =
                (90f + i * 360f / sides) * Mathf.Deg2Rad;

            originalVertices[i + 1] = new Vector3(
                radius * Mathf.Cos(angle),
                radius * Mathf.Sin(angle),
                0f
            );
        }

        int[] triangles = new int[sides * 3];

        for (int i = 0; i < sides; i++)
        {
            triangles[i * 3] = 0;
            triangles[i * 3 + 1] = i + 1;
            triangles[i * 3 + 2] = (i + 1) % sides + 1;
        }

        polygonMesh = new Mesh();
        polygonMesh.name = "Experiment8_Polygon";
        polygonMesh.MarkDynamic();
        polygonMesh.vertices = originalVertices;
        polygonMesh.colors32 = new Color32[]
        {
            new Color32(10, 10, 15, 255),    // Centre: Jet Black
            new Color32(0, 123, 167, 255),  // Cerulean Blue
            new Color32(255, 46, 147, 255), // Neon Rose
            new Color32(0, 123, 167, 255),  // Cerulean Blue
            new Color32(255, 46, 147, 255), // Neon Rose
            new Color32(0, 123, 167, 255)   // Cerulean Blue
        };

        polygonMesh.triangles = triangles;

        polygonMesh.RecalculateNormals();
        polygonMesh.RecalculateBounds();

        meshFilter.mesh = polygonMesh;
    }

    private void CreatePolygonMaterial()
    {
        if (polygonShader == null)
        {
            polygonShader =
                Shader.Find("Experiment8/TransformationUnlit");
        }

        if (polygonShader == null)
        {
            polygonShader =
                Shader.Find("Universal Render Pipeline/Unlit");
        }

        if (polygonShader == null || !polygonShader.isSupported)
        {
            Debug.LogError("No supported polygon shader found.");
            return;
        }

        polygonMaterial = new Material(polygonShader);
        polygonMaterial.name = "Experiment8_Polygon_Material";

        if (polygonMaterial.HasProperty("_BaseColor"))
            polygonMaterial.SetColor("_BaseColor", polygonColor);
        else if (polygonMaterial.HasProperty("_Color"))
            polygonMaterial.SetColor("_Color", polygonColor);

        meshRenderer.enabled = true;
        meshRenderer.material = polygonMaterial;

        Debug.Log("Experiment 8 polygon material assigned.");
    }

    private void ApplyTransformation()
    {
        if (polygonMesh == null || originalVertices == null)
            return;

        Vector3[] transformedVertices =
            new Vector3[originalVertices.Length];

        for (int i = 0; i < originalVertices.Length; i++)
        {
            transformedVertices[i] =
                currentMatrix.MultiplyPoint(originalVertices[i]);
        }

        polygonMesh.vertices = transformedVertices;
        polygonMesh.RecalculateNormals();
        polygonMesh.RecalculateBounds();
    }

    private void ApplyOperation(
        Matrix3x3 operation, string description)
    {
        animateRotation = false;
        currentMatrix = operation * currentMatrix;
        currentOperation = description;
        ApplyTransformation();
    }

    private void TranslatePolygon()
    {
        ApplyOperation(
            Matrix3x3.Translation(1f, 0.5f),
            "Translation");
    }

    private void RotatePolygon()
    {
        ApplyOperation(
            Matrix3x3.Rotation(30f),
            "Rotation: 30 degrees");
    }

    private void RotateAboutPivot()
    {
        ApplyOperation(
            Matrix3x3.RotationAboutPoint(45f, 0.5f, 0.5f),
            "Rotation about pivot (0.5, 0.5)");
    }

    private void ScalePolygon()
    {
        ApplyOperation(
            Matrix3x3.Scaling(1.3f, 0.75f),
            "Non-uniform Scaling");
    }

    private void ReflectPolygon()
    {
        ApplyOperation(
            Matrix3x3.ReflectionX(),
            "Reflection about X-axis");
    }

    private void ReflectAboutYEqualsX()
    {
        ApplyOperation(
            Matrix3x3.ReflectionYEqualsX(),
            "Reflection about y = x");
    }

    private void ShearPolygon()
    {
        ApplyOperation(
            Matrix3x3.Shearing(0.5f),
            "Shearing along X-axis");
    }

    private void CompositeTransformation()
    {
        Matrix3x3 composite =
            Matrix3x3.Translation(0.5f, 0.3f) *
            Matrix3x3.Rotation(30f) *
            Matrix3x3.Scaling(1.2f, 1.2f);

        ApplyOperation(composite, "Composite Transformation");
    }

    private void ResetPolygon()
    {
        animateRotation = false;
        currentMatrix = Matrix3x3.Identity;
        currentOperation = "Original";
        ApplyTransformation();
    }

    private void Update()
    {
        if (!animateRotation)
            return;

        currentMatrix =
            Matrix3x3.Rotation(60f * Time.deltaTime) *
            currentMatrix;

        ApplyTransformation();
    }

    private void OnGUI()
    {
        GUILayout.BeginArea(
            new Rect(12, 12, 270, 430),
            "EXPERIMENT 8",
            GUI.skin.window);

        GUILayout.Label("2D Geometric Transformations");
        GUILayout.Space(5);

        if (GUILayout.Button("1. Translation"))
            TranslatePolygon();

        if (GUILayout.Button("2. Rotation"))
            RotatePolygon();

        if (GUILayout.Button("3. Rotation About Pivot"))
            RotateAboutPivot();

        if (GUILayout.Button("4. Non-uniform Scaling"))
            ScalePolygon();

        if (GUILayout.Button("5. Reflection (X-axis)"))
            ReflectPolygon();

        if (GUILayout.Button("6. Reflection (y = x)"))
            ReflectAboutYEqualsX();

        if (GUILayout.Button("7. Shearing"))
            ShearPolygon();

        if (GUILayout.Button("8. Composite Transformation"))
            CompositeTransformation();

        if (GUILayout.Button("Animate Rotation"))
        {
            animateRotation = !animateRotation;

            currentOperation = animateRotation
                ? "Continuous Rotation"
                : "Animation Paused";
        }

        if (GUILayout.Button("Reset"))
            ResetPolygon();

        GUILayout.Space(8);
        GUILayout.Label("Current: " + currentOperation);

        GUILayout.EndArea();
    }

    private void OnDestroy()
    {
        if (polygonMaterial != null)
            Destroy(polygonMaterial);

        if (polygonMesh != null)
            Destroy(polygonMesh);
    }
}
