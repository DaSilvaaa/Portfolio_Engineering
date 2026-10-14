using System.Security.Authentication;

public record CertInfo(
    string Subject,
    DateTime NotBefore,
    DateTime NotAfter,
    string KeyAlgorithm,
    int KeySize,
    string SignatureAlgorithm,
    SslProtocols Protocol);

public static class CertRules
{
    public static List<string> Evaluate(CertInfo c, DateTime nowUtc, int warnDays = 30)
    {
        var issues = new List<string>();

        if (nowUtc < c.NotBefore)
            issues.Add("certificado ainda não é válido");

        if (nowUtc > c.NotAfter)
            issues.Add("certificado expirado");
        else if ((c.NotAfter - nowUtc).TotalDays <= warnDays)
            issues.Add($"expira em {(int)(c.NotAfter - nowUtc).TotalDays} dias");

        if (c.KeyAlgorithm == "RSA" && c.KeySize < 2048)
            issues.Add($"chave RSA fraca ({c.KeySize} bits)");

        if (c.KeyAlgorithm == "ECDSA" && c.KeySize < 256)
            issues.Add($"chave EC fraca ({c.KeySize} bits)");

        var sig = c.SignatureAlgorithm.ToLowerInvariant();
        if (sig.Contains("sha1") || sig.Contains("md5"))
            issues.Add($"algoritmo de assinatura fraco ({c.SignatureAlgorithm})");

        if (c.Protocol != SslProtocols.Tls12 && c.Protocol != SslProtocols.Tls13)
            issues.Add($"protocolo obsoleto ({c.Protocol})");

        return issues;
    }
}