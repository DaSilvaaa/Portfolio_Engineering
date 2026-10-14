using System.Net.Security;
using System.Net.Sockets;
using System.Security.Cryptography.X509Certificates;

public static class Inspector
{
    public static async Task<(CertInfo Info, SslPolicyErrors Errors)> FetchAsync(string host, int port, TimeSpan timeout)
    {
        using var cts = new CancellationTokenSource(timeout);
        using var tcp = new TcpClient();
        await tcp.ConnectAsync(host, port, cts.Token);

        var errors = SslPolicyErrors.None;
        using var ssl = new SslStream(tcp.GetStream(), false, (_, _, _, e) => { errors = e; return true; });
        await ssl.AuthenticateAsClientAsync(new SslClientAuthenticationOptions { TargetHost = host }, cts.Token);

        var cert = new X509Certificate2(ssl.RemoteCertificate!);
        string alg;
        int bits;

        if (cert.GetRSAPublicKey() is { } rsa)
        {
            alg = "RSA";
            bits = rsa.KeySize;
        }
        else if (cert.GetECDsaPublicKey() is { } ec)
        {
            alg = "ECDSA";
            bits = ec.KeySize;
        }
        else
        {
            alg = cert.PublicKey.Oid.FriendlyName ?? "unknown";
            bits = 0;
        }

        var info = new CertInfo(
            cert.Subject,
            cert.NotBefore.ToUniversalTime(),
            cert.NotAfter.ToUniversalTime(),
            alg,
            bits,
            cert.SignatureAlgorithm.FriendlyName ?? "unknown",
            ssl.SslProtocol);

        return (info, errors);
    }
}