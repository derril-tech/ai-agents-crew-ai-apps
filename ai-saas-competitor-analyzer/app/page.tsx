"use client";

import { useState } from "react";
import { Button, Card, Container, Group, Stack, Text, TextInput, Table, Badge, Title, Anchor, Divider, Loader } from "@mantine/core";
import { IconPlus, IconTrash, IconDownload } from "@tabler/icons-react";

type Competitor = { name: string; url: string; };
type AnalyzeResponse = {
  normalized: any[];
  feature_matrix: { matrix: Record<string, Record<string, boolean>>; feature_categories: Record<string, string>; };
  comparison: { price_efficiency: Record<string, number>; cheapest_for_baseline?: string; best_for_advanced?: string; };
  strategy: { gap_features_to_add: string[]; pricing_levers: string[]; gtms: string[]; risks: string[]; };
  report: { pdf_path: string; json_export_path: string; charts: string[]; title: string; };
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export default function Home() {
  const [industry, setIndustry] = useState("Helpdesk SaaS");
  const [competitors, setCompetitors] = useState<Competitor[]>([
    { name: "FreshHelp", url: "https://example.com" },
    { name: "Supportly", url: "https://example.org" },
  ]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  const addRow = () => setCompetitors((c) => [...c, { name: "", url: "" }]);
  const removeRow = (i: number) => setCompetitors((c) => c.filter((_, idx) => idx !== i));
  const updateRow = (i: number, key: keyof Competitor, val: string) =>
    setCompetitors((c) => c.map((row, idx) => (idx === i ? { ...row, [key]: val } : row)));

  const runAnalysis = async () => {
    setLoading(true); setResult(null);
    try {
      const payload = {
        industry,
        competitors: competitors.filter((c) => c.name && c.url).map((c) => ({ name: c.name, url: c.url }))
      };
      const r = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await r.json();
      setResult(data);
    } catch (e) {
      console.error(e);
      alert("Analysis failed. Check console.");
    } finally {
      setLoading(false);
    }
  };

  const renderEfficiency = () => {
    if (!result) return null;
    const entries = Object.entries(result.comparison.price_efficiency).sort((a, b) => b[1] - a[1]);
    return (
      <Table highlightOnHover withTableBorder withColumnBorders>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Competitor</Table.Th>
            <Table.Th>Features per $ (cheapest plan)</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {entries.map(([name, score]) => (
            <Table.Tr key={name}>
              <Table.Td>{name}</Table.Td>
              <Table.Td>{score}</Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
    );
  };

  return (
    <Container size="lg" py="xl">
      <Stack gap="lg">
        <Title order={2}>AI SaaS Competitor Analyzer</Title>
        <Card withBorder>
          <Stack>
            <Group grow>
              <TextInput label="Industry" value={industry} onChange={(e) => setIndustry(e.currentTarget.value)} />
            </Group>
            <Divider my="xs" label="Competitors" />
            <Stack>
              {competitors.map((row, i) => (
                <Group key={i} align="flex-end">
                  <TextInput label="Name" value={row.name} onChange={(e) => updateRow(i, "name", e.currentTarget.value)} style={{ flex: 1 }} />
                  <TextInput label="Homepage / Pricing URL" value={row.url} onChange={(e) => updateRow(i, "url", e.currentTarget.value)} style={{ flex: 2 }} />
                  <Button variant="light" color="red" onClick={() => removeRow(i)} leftSection={<IconTrash size={16} />}>Remove</Button>
                </Group>
              ))}
              <Group>
                <Button variant="default" leftSection={<IconPlus size={16} />} onClick={addRow}>Add competitor</Button>
                <Button onClick={runAnalysis} disabled={loading}>
                  {loading ? <Loader size="sm" /> : "Run analysis"}
                </Button>
              </Group>
            </Stack>
          </Stack>
        </Card>

        {result && (
          <>
            <Card withBorder>
              <Stack gap="sm">
                <Text fw={700}>Highlights</Text>
                <Group>
                  <Badge color="green">Cheapest baseline: {result.comparison.cheapest_for_baseline ?? "n/a"}</Badge>
                  <Badge color="blue">Best for advanced: {result.comparison.best_for_advanced ?? "n/a"}</Badge>
                </Group>
              </Stack>
            </Card>

            <Card withBorder>
              <Text fw={700} mb="sm">Price Efficiency</Text>
              {renderEfficiency()}
            </Card>

            <Card withBorder>
              <Text fw={700} mb="sm">Strategy Recommendations</Text>
              <Stack>
                <div>
                  <Text fw={600}>Gap features to add</Text>
                  <Group>{result.strategy.gap_features_to_add.map((f) => <Badge key={f}>{f}</Badge>)}</Group>
                </div>
                <div>
                  <Text fw={600}>Pricing levers</Text>
                  <ul>{result.strategy.pricing_levers.map((p, i) => <li key={i}>{p}</li>)}</ul>
                </div>
                <div>
                  <Text fw={600}>GTM angles</Text>
                  <ul>{result.strategy.gtms.map((g, i) => <li key={i}>{g}</li>)}</ul>
                </div>
                <div>
                  <Text fw={600}>Risks</Text>
                  <ul>{result.strategy.risks.map((r, i) => <li key={i}>{r}</li>)}</ul>
                </div>
              </Stack>
            </Card>

            <Card withBorder>
              <Text fw={700} mb="sm">Artifacts</Text>
              <Stack gap="xs">
                <Group>
                  <Anchor href={`${API_BASE}${result.report.pdf_path.replace("http://localhost:8000","")}`} target="_blank">
                    <Button leftSection={<IconDownload size={16} />}>Open PDF report</Button>
                  </Anchor>
                  <Anchor href={`${API_BASE}${result.report.json_export_path.replace("http://localhost:8000","")}`} target="_blank">
                    <Button variant="light">Open JSON export</Button>
                  </Anchor>
                </Group>
                <Group>
                  {result.report.charts.map((p) => (
                    <Anchor key={p} href={`${API_BASE}${p.replace("http://localhost:8000","").replace("\\","/")}`} target="_blank">
                      <Badge variant="light">Chart</Badge>
                    </Anchor>
                  ))}
                </Group>
              </Stack>
            </Card>
          </>
        )}
      </Stack>
    </Container>
  );
}
