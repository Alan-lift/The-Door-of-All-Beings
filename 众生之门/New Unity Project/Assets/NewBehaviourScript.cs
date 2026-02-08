using UnityEngine;

public class CameraController : MonoBehaviour
{
    [Header("移动设置")]
    public float moveSpeed = 5f;      // 移动速度
    public float fastMoveSpeed = 10f; // 加速移动速度
    public float rotateSpeed = 100f;  // 旋转速度

    [Header("高度控制")]
    public float heightChangeSpeed = 3f;
    public float minHeight = 2f;
    public float maxHeight = 20f;

    [Header("边界限制")]
    public bool useBoundary = true;
    public Vector2 boundaryMin = new Vector2(-50, -50);
    public Vector2 boundaryMax = new Vector2(50, 50);

    void Update()
    {
        HandleCameraMovement();
        HandleCameraRotation();
        HandleHeightControl();
        ClampCameraPosition();
    }

    void HandleCameraMovement()
    {
        // 获取方向键输入
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        // 如果使用鼠标控制，可以取消注释下面这行
        // if (Input.GetMouseButton(1)) // 右键按住移动

        // 计算移动速度（Shift加速）
        float currentSpeed = Input.GetKey(KeyCode.LeftShift) ? fastMoveSpeed : moveSpeed;

        // 计算移动方向
        Vector3 moveDirection = new Vector3(horizontal, 0, vertical);

        // 如果方向有输入
        if (moveDirection.magnitude > 0.1f)
        {
            // 根据摄像机的朝向移动（这样WSAD更符合直觉）
            Vector3 forward = transform.forward;
            Vector3 right = transform.right;

            forward.y = 0; // 保持水平移动
            right.y = 0;
            forward.Normalize();
            right.Normalize();

            // 计算最终移动方向
            Vector3 movement = (forward * vertical + right * horizontal).normalized;

            // 应用移动
            transform.position += movement * currentSpeed * Time.deltaTime;
        }
    }

    void HandleCameraRotation()
    {
        // Q/E旋转摄像机
        if (Input.GetKey(KeyCode.Q))
        {
            transform.Rotate(Vector3.up, -rotateSpeed * Time.deltaTime, Space.World);
        }
        if (Input.GetKey(KeyCode.E))
        {
            transform.Rotate(Vector3.up, rotateSpeed * Time.deltaTime, Space.World);
        }

        // 鼠标右键拖拽旋转
        if (Input.GetMouseButton(1)) // 右键
        {
            float mouseX = Input.GetAxis("Mouse X") * rotateSpeed * Time.deltaTime;
            float mouseY = Input.GetAxis("Mouse Y") * rotateSpeed * Time.deltaTime;

            // 水平旋转
            transform.Rotate(Vector3.up, mouseX, Space.World);

            // 垂直旋转（有角度限制）
            float currentXRotation = transform.localEulerAngles.x;
            float newXRotation = currentXRotation - mouseY;

            // 限制垂直旋转角度 (-60° 到 80°)
            if (newXRotation > 80 && newXRotation < 180)
                newXRotation = 80;
            if (newXRotation < 300 && newXRotation > 180)
                newXRotation = 300; // 300 = -60

            transform.localEulerAngles = new Vector3(
                newXRotation,
                transform.localEulerAngles.y,
                0
            );
        }
    }

    void HandleHeightControl()
    {
        // PageUp/PageDown 控制高度
        if (Input.GetKey(KeyCode.PageUp) || Input.GetKey(KeyCode.E))
        {
            Vector3 newPosition = transform.position;
            newPosition.y += heightChangeSpeed * Time.deltaTime;
            newPosition.y = Mathf.Clamp(newPosition.y, minHeight, maxHeight);
            transform.position = newPosition;
        }
        if (Input.GetKey(KeyCode.PageDown) || Input.GetKey(KeyCode.Q))
        {
            Vector3 newPosition = transform.position;
            newPosition.y -= heightChangeSpeed * Time.deltaTime;
            newPosition.y = Mathf.Clamp(newPosition.y, minHeight, maxHeight);
            transform.position = newPosition;
        }

        // 鼠标滚轮控制高度
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        if (Mathf.Abs(scroll) > 0.01f)
        {
            Vector3 newPosition = transform.position;
            newPosition.y -= scroll * heightChangeSpeed * 10f;
            newPosition.y = Mathf.Clamp(newPosition.y, minHeight, maxHeight);
            transform.position = newPosition;
        }
    }

    void ClampCameraPosition()
    {
        if (useBoundary)
        {
            Vector3 pos = transform.position;
            pos.x = Mathf.Clamp(pos.x, boundaryMin.x, boundaryMax.x);
            pos.z = Mathf.Clamp(pos.z, boundaryMin.y, boundaryMax.y);
            transform.position = pos;
        }
    }

    // 在Scene视图中显示边界（仅编辑器）
    void OnDrawGizmosSelected()
    {
        if (useBoundary)
        {
            Gizmos.color = Color.yellow;
            Vector3 center = new Vector3(
                (boundaryMin.x + boundaryMax.x) * 0.5f,
                transform.position.y,
                (boundaryMin.y + boundaryMax.y) * 0.5f
            );
            Vector3 size = new Vector3(
                boundaryMax.x - boundaryMin.x,
                0.1f,
                boundaryMax.y - boundaryMin.y
            );
            Gizmos.DrawWireCube(center, size);
        }
    }
}