import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.Console;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.SecureRandom;
import java.util.Arrays;

public class Vault {
    private static final byte[] MAGIC = {'V', 'L', 'T', '1'};
    private static final int SALT_LEN = 16;
    private static final int IV_LEN = 12;
    private static final int ITERATIONS = 310_000;
    private static final int KEY_BITS = 256;
    private static final int TAG_BITS = 128;

    static SecretKey derive(char[] password, byte[] salt) throws Exception {
        PBEKeySpec spec = new PBEKeySpec(password, salt, ITERATIONS, KEY_BITS);
        try {
            byte[] k = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
            return new SecretKeySpec(k, "AES");
        } finally {
            spec.clearPassword();
        }
    }

    static byte[] encrypt(byte[] plain, char[] password) throws Exception {
        SecureRandom rnd = new SecureRandom();
        byte[] salt = new byte[SALT_LEN];
        byte[] iv = new byte[IV_LEN];
        rnd.nextBytes(salt);
        rnd.nextBytes(iv);

        Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
        c.init(Cipher.ENCRYPT_MODE, derive(password, salt), new GCMParameterSpec(TAG_BITS, iv));
        c.updateAAD(MAGIC);
        byte[] ct = c.doFinal(plain);

        return ByteBuffer.allocate(MAGIC.length + SALT_LEN + IV_LEN + ct.length)
                .put(MAGIC).put(salt).put(iv).put(ct).array();
    }

    static byte[] decrypt(byte[] blob, char[] password) throws Exception {
        if (blob.length < MAGIC.length + SALT_LEN + IV_LEN + TAG_BITS / 8
                || !Arrays.equals(Arrays.copyOfRange(blob, 0, MAGIC.length), MAGIC)) {
            throw new IllegalArgumentException("Formato inválido ou assinatura mágica não reconhecida");
        }

        int o = MAGIC.length;
        byte[] salt = Arrays.copyOfRange(blob, o, o + SALT_LEN); 
        o += SALT_LEN;
        byte[] iv = Arrays.copyOfRange(blob, o, o + IV_LEN); 
        o += IV_LEN;

        Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
        c.init(Cipher.DECRYPT_MODE, derive(password, salt), new GCMParameterSpec(TAG_BITS, iv));
        c.updateAAD(MAGIC);
        return c.doFinal(blob, o, blob.length - o);
    }

    static char[] readPassword() {
        Console c = System.console();
        if (c != null) return c.readPassword("Password: ");
        String env = System.getenv("VAULT_PASSWORD");
        if (env == null) throw new IllegalStateException("Sem terminal interativo: defina a variável VAULT_PASSWORD");
        return env.toCharArray();
    }

    public static void main(String[] a) throws Exception {
        if (a.length != 3 || !(a[0].equals("enc") || a[0].equals("dec"))) {
            System.err.println("uso: Vault <enc|dec> <entrada> <saída>");
            System.exit(2);
        }
        char[] pw = readPassword();
        byte[] in = Files.readAllBytes(Path.of(a[1]));
        byte[] out = a[0].equals("enc") ? encrypt(in, pw) : decrypt(in, pw);
        Files.write(Path.of(a[2]), out);
        Arrays.fill(pw, '\0');
    }
}