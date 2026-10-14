using System.Security.Authentication;
using Xunit;

public class CertRulesTests
{
    static readonly DateTime Now = new(2026, 1, 1, 0, 0, 0, DateTimeKind.Utc);

    static CertInfo Make(
        DateTime? notAfter = null,
        string alg = "RSA",
        int bits = 2048,
        string sig = "sha256RSA",
        SslProtocols proto = SslProtocols.Tls13)
        => new("CN=test", Now.AddYears(-1), notAfter ?? Now.AddDays(200), alg, bits, sig, proto);

    [Fact]
    public void HealthyCertHasNoIssues() => Assert.Empty(CertRules.Evaluate(Make(), Now));

    [Fact]
    public void DetectsExpired() =>
        Assert.Contains("certificado expirado", CertRules.Evaluate(Make(Now.AddDays(-1)), Now));

    [Fact]
    public void DetectsExpiringSoon() =>
        Assert.Contains(CertRules.Evaluate(Make(Now.AddDays(10)), Now), i => i.StartsWith("expira em"));

    [Fact]
    public void DetectsWeakRsa() =>
        Assert.Contains(CertRules.Evaluate(Make(bits: 1024), Now), i => i.Contains("RSA fraca"));

    [Fact]
    public void AcceptsEcdsa256() =>
        Assert.Empty(CertRules.Evaluate(Make(alg: "ECDSA", bits: 256), Now));

    [Fact]
    public void DetectsSha1Signature() =>
        Assert.Contains(CertRules.Evaluate(Make(sig: "sha1RSA"), Now), i => i.Contains("assinatura fraco"));

    [Fact]
    public void DetectsLegacyProtocol() =>
        Assert.Contains(CertRules.Evaluate(Make(proto: (SslProtocols)768), Now), i => i.Contains("obsoleto"));
}