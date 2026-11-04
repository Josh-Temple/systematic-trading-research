// Source-only JForex strategy. No order submission, no direction/return calculation.
// JForex runtime compatibility must be verified inside JForex before treating as live-tested.
package jforex;

import com.dukascopy.api.*;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.time.Instant;
import java.util.List;
import java.util.Locale;

@RequiresFullAccess
public class JForexUsdJpyBoundedSource implements IStrategy {
    // Predeclared ordinary weekday window. Do not choose another date based on prices.
    private static final long FROM_MS = Instant.parse("2024-01-15T12:59:00Z").toEpochMilli();
    private static final long TO_MS = Instant.parse("2024-01-15T13:01:00Z").toEpochMilli();
    private static final int MAX_TICKS = 100000;
    private static final String HEADER =
        "timestamp_utc_ms,bid,ask,bid_volume,ask_volume,instrument";

    @Configurable("Output CSV file (must not already exist)")
    public String outputFile = "USDJPY_20240115_1259-1301_UTC.csv";

    @Override
    public void onStart(IContext context) throws JFException {
        try {
            List<ITick> ticks = context.getHistory().getTicks(Instrument.USDJPY, FROM_MS, TO_MS);
            if (ticks == null || ticks.isEmpty() || ticks.size() > MAX_TICKS) {
                context.getConsole().getErr().println(
                    "BLOCKED: empty/oversized bounded historical tick response; no CSV created");
                return;
            }
            for (ITick tick : ticks) {
                if (tick == null || tick.getTime() < FROM_MS || tick.getTime() > TO_MS ||
                    !Double.isFinite(tick.getBid()) || !Double.isFinite(tick.getAsk()) ||
                    tick.getBid() <= 0 || tick.getAsk() < tick.getBid() ||
                    !Double.isFinite(tick.getBidVolume()) || !Double.isFinite(tick.getAskVolume()) ||
                    tick.getBidVolume() < 0 || tick.getAskVolume() < 0) {
                    context.getConsole().getErr().println(
                        "BLOCKED: structurally invalid tick; no CSV created");
                    return;
                }
            }
            Path target = Paths.get(outputFile).toAbsolutePath();
            // CREATE_NEW never overwrites a previous source artifact.
            try (BufferedWriter out = Files.newBufferedWriter(target, StandardCharsets.UTF_8,
                    StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE)) {
                out.write(HEADER);
                out.newLine();
                for (ITick tick : ticks) {
                    out.write(String.format(Locale.ROOT, "%d,%s,%s,%s,%s,USDJPY%n",
                        tick.getTime(), Double.toString(tick.getBid()),
                        Double.toString(tick.getAsk()), Double.toString(tick.getBidVolume()),
                        Double.toString(tick.getAskVolume())));
                }
            }
            context.getConsole().getOut().println("SOURCE_ONLY_CSV_WRITTEN; ticks="
                    + ticks.size() + "; file=" + target);
        } catch (IOException | RuntimeException ex) {
            context.getConsole().getErr().println(
                "BLOCKED: source-only export failed: " + ex.getClass().getSimpleName());
        } finally {
            // Stop immediately; never execute a trade or create continuous signal collection.
            context.stop();
        }
    }

    @Override public void onTick(Instrument instrument, ITick tick) throws JFException { }
    @Override public void onBar(Instrument instrument, Period period,
            IBar askBar, IBar bidBar) throws JFException { }
    @Override public void onMessage(IMessage message) throws JFException { }
    @Override public void onAccount(IAccount account) throws JFException { }
    @Override public void onStop() throws JFException { }
}
