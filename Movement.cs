using UnityEngine;

public class Movement : MonoBehaviour
{
    RigidBody2D rb;
    public float speed;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    void FixedUpdate()
    {
        rb.velocity = Vector2.down * speed;
    }
}
