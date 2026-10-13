import org.junit.jupiter.api.Test;
import javax.crypto.AEADBadTagException;
import java.nio.charset.StandardCharsets;
import static org.junit.jupiter.api.Assertions.*;

class VaultTest {
    @Test
    void roundTrip() throws Exception {
        byte[] original = "mensagem confidencial".getBytes(StandardCharsets.UTF_8);
        byte[] blob = Vault.encrypt(original, "senhaSegura123".toCharArray());
        assertArrayEquals(original, Vault.decrypt(blob, "senhaSegura123".toCharArray()));
    }

    @Test
    void wrongPasswordFails() throws Exception {
        byte[] blob = Vault.encrypt(new byte[]{1, 2, 3, 4}, "correta".toCharArray());
        assertThrows(Exception.class, () -> Vault.decrypt(blob, "errada".toCharArray()));
    }

    @Test
    void tamperedCiphertextFails() throws Exception {
        byte[] blob = Vault.encrypt(new byte[]{1, 2, 3, 4}, "chave".toCharArray());
        // Adulterar o último byte (tag de integridade GCM)
        blob[blob.length - 1] ^= 1;
        assertThrows(Exception.class, () -> Vault.decrypt(blob, "chave".toCharArray()));
    }
}