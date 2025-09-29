export interface TariffConfig {
  flat?: { rate: number; fixed_fee: number };
  tou?: { peak_rate: number; shoulder_rate: number; offpeak_rate: number; fixed_fee: number };
  tiered?: { tiers: [number, number][]; fixed_fee: number };
}

export interface UsageTrend {
  timestamp: string;
  kWh: number;
}

export interface BillResponse {
  bill: number;
  breakdown: Record<string, number> | null;
}