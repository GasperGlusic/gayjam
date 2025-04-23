using UnityEngine;

public class Blak : MonoBehaviour
{
   int i, je = 0;
   private float cas = 15, casD = 60;
   private GameObject objekt;

void Start() {
    objekt = GameObject.FindGameObjectWithTag("Enemy");
}

    void Detonacija() {
        i = UnityEngine.Random.Range(1, 3);
        je = 0;
        if(i == 1) {
            kloniranje();
        }
    }

    void kloniranje()
    {
       Instantiate(objekt, gameObject.transform.position, Quaternion.identity);
       Destroy(objekt, casD);
    }

    void Update() {
        if(je == 0) {
            je = 1;
            Invoke("Detonacija", cas);
        }
    }

}

